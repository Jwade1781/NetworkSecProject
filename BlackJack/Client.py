###############################################################################
# Current orders of operations:
# [1] Establish Connection with Host
# [2] Receive the hosts public key (No Decryption)
# [3] Generate clients public and private keys
# [4] Send the clientPublicKey to host (Encrypt hostPublicKey)
# [5] Receive prompt of what the client would like to do (Decrypt clientPrivateKey)
# [6] Send Response to Host with request (Encrypt hostPublicKey)
#       A. Login
#       B. Signup
#
# [6.A] A. Receive Login userID prompt and send userID (Decrypt clientPrivateKey / Encrypt hostPublicKey)
#       B. Receive Login password prompt and send password (Decrypt clientPrivateKey / Encrypt hostPublicKey)
#       C. Receive Response (Decrypt clientPrivateKey)
#           if response is successful:
#               Goto step [7]
#           else:
#               Attempt step [6.A] again
# [6.B] A. Receive Prompt to enter userID and send the inputted userID (Decrypt clientPrivateKey / Encrypt hostPublicKey)
#       B. Receive prompt on either enter a password or the userID is already in use (Decrypt clientPrivateKey)
#          If in use repeat second half of step A
#       C. If not in use, input the desired password, validate it is at least 8 chars in length
#       D. Send Password to Host (Encrypt hostPublicKey)
#
# [7] Start blackjack game
###############################################################################

class Client:
    def __init__(self):
        from Communication import Communication
        from Encryption import Encryption
        PORT_NUMBER = 12371
        
        # [1] Establish connection with host
        connection = self.Establish_Connection(portNumber = PORT_NUMBER)
        communication = Communication(connection)
        
        # [2] Receive Host public Key as a string, dump to a temp file, then open
        strHostPublicKey = communication.Receive_Message(False, None, None)
        self.Dump_Key(privateKey= None, publicKey=strHostPublicKey, keyType="host")
        hostPublicKey = self.Load_Key(keyName="Public", keyType="host")
        
            # [3] Generate clients (string) public and private keys. Dump to temp file and load the private key object
        strClientPrivateKey, strClientPublicKey = Encryption().Generate_RSA_Keys(keySize=4096, exponent=65537)
        self.Dump_Key(privateKey = strClientPrivateKey, publicKey=strClientPublicKey, keyType="client")
        clientPrivateKey = self.Load_Key(keyName = "Private", keyType = "client")
        
            # [4] Send string client public key to host .. Encrypt with hostPublicKey
        communication.Send_Message(encryptionNeeded=False, encryptionAlgorithm=None, key=None, message=strClientPublicKey)
        
            # [5] Receive prompt of what the client would like to do (Decrypt Client privateKey)
        response = communication.Receive_Message(encryptionNeeded=True, encryptionAlgorithm="RSA", key=clientPrivateKey)
        userInput = ""
        while userInput != "1" and userInput != "2":
            userInput=input(response)
        
            # [6] Send Response back to Host with inputted request (Encrypt hostPublicKey)
        communication.Send_Message(encryptionNeeded=True, encryptionAlgorithm="RSA", key=hostPublicKey, message=userInput)
        if userInput == "1": self.User_Login(communication, hostPublicKey, clientPrivateKey)
        if userInput == "2": self.New_User_Signup(communication, hostPublicKey, clientPrivateKey)
        
            # [7] Start blackjack game
        from BlackJack_Client import BlackJack
        blackJack = BlackJack(communication, hostPublicKey, clientPrivateKey)
        communication.Close_Connection()
        
        print("Not connected with host")
        
###############################################################################        
# Connects to the host
    def Establish_Connection(self, portNumber):
        import socket
        connection = socket.socket()
        host = socket.gethostname()
        print('Connecting to port:', portNumber)
        connection.connect((host, portNumber))
        return connection
    
###############################################################################
# Dumps the key as a public/private key into a temp file that will be reloaded 
# later into key object
    def Dump_Key(self, privateKey, publicKey, keyType):
        PATH = "client/clientTemp/"
        if publicKey is not None:
            keyFile = open(PATH + keyType + "PublicKey.pem", "w")
            keyFile.write(publicKey)
            keyFile.close()
        
        if privateKey is not None:
            keyFile = open(PATH + keyType + "PrivateKey.pem", "w")
            keyFile.write(privateKey)
            keyFile.close()

###############################################################################
# Loads the key from the file as a key object and returns it
    def Load_Key(self, keyName, keyType):
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization
        PATH = "client/clientTemp/"
        with open(PATH + keyType + keyName + "Key.pem", "rb") as keyFile:
            if keyName == "Public":
                key = serialization.load_pem_public_key(
                    data=keyFile.read(), 
                    backend=default_backend()
                )
            else:
                key = serialization.load_pem_private_key(
                    data=keyFile.read(),
                    password=None,
                    backend=default_backend()
                )
        return key
############################################################################### 
# Gather the Users credentials, generate a SHA256 hash value with the inputs
# And compare the generated hash with the hash value from the passwords file
    def User_Login(self, communication, hostPublicKey, clientPrivateKey):        
        loggedIn = False
        userID = None
        while(not loggedIn):
            # Get prompt to enter both userID and password and send the inputs back to host
            userID = input(communication.Receive_Message(True, "RSA", clientPrivateKey))
            communication.Send_Message(True, "RSA", hostPublicKey, userID)
            
            password = input(communication.Receive_Message(True, "RSA", clientPrivateKey))
            communication.Send_Message(True, "RSA", hostPublicKey, password)
            
            response = communication.Receive_Message(True, "RSA", clientPrivateKey)
            if response == "True": loggedIn = True
            else: print("You have failed to loggin.. Try again")
        print("Welcome", userID, "\nYou have logged in successfully", end="\n\n")

############################################################################### 
    def New_User_Signup(self, communication, hostPublicKey, clientPrivateKey):
        self.Create_User_Credentials(communication, hostPublicKey, clientPrivateKey, "userID")
        self.Create_User_Credentials(communication, hostPublicKey, clientPrivateKey, "password")
        print(communication.Receive_Message(True, "RSA", clientPrivateKey))
        
############################################################################### 
    def Create_User_Credentials(self, communication, hostPublicKey, clientPrivateKey, credentialType):
        sentInvalidCredential = True
        while sentInvalidCredential: 
            response = (communication.Receive_Message(True, "RSA", clientPrivateKey))
            credential = None
            while credential == None or credential == "" or (credentialType == "password" and len(credential) < 12):
                credential = input(response)
                
            communication.Send_Message(True, "RSA", hostPublicKey, credential)
            response = communication.Receive_Message(True, "RSA", clientPrivateKey) # response on whether the entered userID was accepted or not
            
            # Sent a valid userID, break the loop
            if response == "False": sentInvalidCredential = False
            
            # Send an invalid userID, print the reasoning and continue to resubmit another user ID
            else: print("\nThe", credentialType, "was not accepted. Please try another\n")