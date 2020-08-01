###############################################################################
# Current orders of operations:
# [1] Generate a Public / Private Key Pair 
# [2] Listen for any attempted client connections
# [3] Send Connected Client the generated publicHostKey (Unencrypted)
# [4] Receive the generated encrypted clientPublicKey from client (Decrypt hostsPrivateKey)
#
# [5] Ask User what they want to do: (Encrypt clientPublicKey)
#       A. Login
#       B. Signup
#
# [6.A] A. Ask User to input UserID (Encrypt clientPublicKey)
#       B. Receive UserID (Decrypt hostPrivateKey)
#       C. Ask User to input Password (Encrypt clientPublicKey)
#       D. Receive Password (Decrypt hostPrivateKey)
#       E. Open password file and look for any matching userID's
#           [Success] Pull row (userID, salt, hash)
#                     Append salt with inputted password and generate a hash value
#                     if generated hash and the hash in file do not match, go to [unsuccess]
#                     else go to step [7]
#
#           [Unsuccess] Tell client that login was unsuccessful
#                       Raise amounts of attempts tried
#                       if maxed attempts are reached, close connection
#                       Else repeat step [6.A]
#
# [6.B] A. Ask User for the User ID, retrieve and decrypt
#       B. Open password file and make sure UserID is not currently in use
#          Send [True] if good to use or [False] if the userID is already in use (Encrypt clientPublicKey)
#       C. Ask User for the password, retrieve and decrypt 
#          Compare to common password file, send [True] if good or [False] if it appears in file (Encrypt clientPublicKey)
#       D. Generate random salt value that is not already in use in the password file
#       E. Hash the inputted password with the unique Salt value
#       F. Store the userID, salt, and generated hash value in password file
#
# [7] Start blackjack game will update later with operations
###############################################################################
class Host:
    def __init__(self):
        from Communication import Communication
        from Encryption import Encryption
       
        PORT_NUMBER = 12371
        self.connections = []
        
        # [1] Generate asymmetric key pair
        strHostPrivateKey, strHostPublicKey = Encryption().Generate_RSA_Keys(keySize=4096, exponent=65537)
        self.Dump_Keys(strHostPrivateKey, strHostPublicKey, "host")
        #hostPublicKey = self.Load_Key(keyName="Public", keyType="host")
        hostPrivateKey = self.Load_Key("Private", "host")
        blacklist = []
        
        while True:
            
                # [2] Listen for attempted client connections
            clientConnection, address = self.Listen_For_Connection(PORT_NUMBER)
            communication = Communication(clientConnection)   
            print(address[0], "has connected", end="\n\n")
            if address[0] in blacklist:
                print("Attempted connection from black listed source", address[0], end="\n\n")
                communication.Close_Connection()
                continue
            
                # [3] Send unencrypted public key
            communication.Send_Message(False, None, None, strHostPublicKey)
                #self.Send_Message(connection=clientConnection, encryptionNeeded=False, encryptionAlgorithm=None, key=None, message=publicKey, messageType="key")
        
                # [4] Receive client's public key and decrypt with host privatekey
            strClientPublicKey = communication.Receive_Message(False, None, None)
            self.Dump_Keys(None, strClientPublicKey, "client")
            clientPublicKey = self.Load_Key("Public", "client")
    
                # [5] Ask User what they would like to do: signup / login .. Return the logged in user
                # if user was unsuccessful at logging in, close connection and wait for new connection
            userID = self.Get_User_Option(communication, clientPublicKey, hostPrivateKey)
            if userID is None: 
                print("No user logged in, looking for another connection")                    
                blacklist.append(address[0])
                print("Added", address[0], "to blacklist")
                communication.Close_Connection()
        
            else:
                print("Starting blackjack")
                from BlackJack_Host import BlackJack
                hostBlackJack = BlackJack(communication, userID, clientPublicKey, hostPrivateKey)
                communication.Close_Connection()
            #except:
            #    communication.Close_Connection()
            #    continue
###############################################################################
# Wait for a connection to be made onto the listening port
    def Listen_For_Connection(self, portNumber):
        import socket
        hostSocket = socket.socket()
        host = socket.gethostname()
        port = portNumber
        hostSocket.bind((host, port))
        
        print('Listening to port:', portNumber)
        MAX_QUEUE = 1
        hostSocket.listen(MAX_QUEUE)
        
        connection, address = hostSocket.accept()      
        self.connections.append(address)
        return connection, address
    
###############################################################################
# Dump the Private / Public Keys as a string into the appropriate temp files
    def Dump_Keys(self, privateKey, publicKey, keyType):
        PATH = "host/hostTemp/"
        keyFile = open(PATH + keyType + "PublicKey.pem", "w")
        keyFile.write(publicKey)
        keyFile.close()
        
        if privateKey is not None:
            keyFile = open(PATH + keyType + "PrivateKey.pem", "w")
            keyFile.write(privateKey)
            keyFile.close()

###############################################################################
# Load the key objects from the appropriate file
    def Load_Key(self, keyName, keyType):
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization
        PATH = "host/hostTemp/"
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
# Asks the user what they would like to do: either login or signup &&
# returns their userID if successful at either, else it will return None

    def Get_User_Option(self, communication, clientPublicKey, hostPrivateKey):
        message = "What would you like to do?\n[1] Login\n[2] Signup\n"
        communication.Send_Message(True, "RSA", clientPublicKey, message)
        response = communication.Receive_Message(True, "RSA", hostPrivateKey)
        # User wants to login
        if response == "1": return self.User_Login(communication, clientPublicKey, hostPrivateKey)
        
        # User wants to sign up
        if response == "2": return self.New_User_Signup(communication, clientPublicKey, hostPrivateKey)

############################################################################### 
# Gather the Users credentials, generate a SHA256 hash value with the inputs
# And compare the generated hash with the hash value from the passwords file
    def User_Login(self, communication, clientPublicKey, hostPrivateKey):
        FILENAME = "host/users.csv"
        MOST_ATTEMPTS = 3
        for attempts in range (0, MOST_ATTEMPTS):
            #print("Attempts remaining:", MOST_ATTEMPTS - attempts)     

            # Asks the user to enter their credentials and store it
            message = "Please enter your User ID\n"
            communication.Send_Message(True, "RSA", clientPublicKey, message)
            userID = communication.Receive_Message(True, "RSA", hostPrivateKey)
            
            message = "Please enter your Password\n"
            communication.Send_Message(True, "RSA", clientPublicKey, message)
            password = communication.Receive_Message(True, "RSA", hostPrivateKey)
            #print("Entered credentials: ", userID, password)
            
            userAuthenticated = self.Authenticate_User(userID, password, FILENAME)
            if userAuthenticated:
                message = "You have logged into " + userID
                communication.Send_Message(True, "RSA", clientPublicKey, "True")
                print("User", userID, "has logged in")
                return userID
            else:
                communication.Send_Message(True, "RSA", clientPublicKey, "False")
                if attempts < MOST_ATTEMPTS:
                    message = "You have failed to login.. Please try again"
                    #communication.Send_Message(True, "RSA", clientPublicKey, message)
                else:
                    message = "You have failed to login.. Please try again later"
                    #communication.Send_Message(True, "RSA", clientPublicKey, message)
        print("Connected user failed credential check")
        communication.Close_Connection()
        return None
        
############################################################################### 
# Allows the user to signup. 
    def New_User_Signup(self, communication, clientPublicKey, hostPrivateKey):
        import csv
        USERFILE = "host/users.csv"
        CREDITSFILE = "host/Credits.csv"
        PASSWORDFILE = "host/common_passwords.csv"
        # Ask user to enter the ID that they would like to use & check to see if it's already in use
        # If it was already used, keep trying until a new userID is created
        receivedInvalidUserName = True
        while receivedInvalidUserName:
            message = "Enter the User ID that you would like to use\n"
            communication.Send_Message(True, "RSA", clientPublicKey, message)
            userID = communication.Receive_Message(True, "RSA", hostPrivateKey)
            receivedInvalidUserName = self.Check_Credential(userID, USERFILE)

            #Received a valid username, break loop and get password
            if receivedInvalidUserName: communication.Send_Message(True, "RSA", clientPublicKey, "True")    
            
            # Received invalid username, give reason and let user resubmit a new username
            else: communication.Send_Message(True, "RSA", clientPublicKey, "False")

        # Ask user to enter the password that they would like to use
        receivedInvalidPassword = True
        while receivedInvalidPassword:
            message = "Enter a Password with at least 12 characters that you would like to use\n"
            communication.Send_Message(True, "RSA", clientPublicKey, message)
            password = communication.Receive_Message(True, "RSA", hostPrivateKey)
            # Checks to see if password is in file, if true the password will need to be reprovided 
            receivedInvalidPassword = self.Check_Credential(password, PASSWORDFILE)
            
            if receivedInvalidPassword: 
                communication.Send_Message(True, "RSA", clientPublicKey, "True")
                print("Password provided is too simple")
            else: communication.Send_Message(True, "RSA", clientPublicKey, "False")
        
        message = "You have successfully signed up.\n"
        communication.Send_Message(True, "RSA", clientPublicKey, message)
        salt = self.Generate_Salt(USERFILE)
        import hashlib
        hashValue = (str(salt) + password).encode()
        hashValue = hashlib.sha256(hashValue)
        hashValue = hashValue.hexdigest()        
        newRowValues = [userID, salt, hashValue]
        with open(USERFILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(newRowValues)
            file.close()
        
        # Append the credits file so the user starts with a set of credits to spend
        newUserCredits = 100
        newRowValues = [userID, newUserCredits]
        with open(CREDITSFILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(newRowValues)
            file.close()
        return userID
###############################################################################
# Generates a random salt value that has a range of 64 bits
# Look to see if the salt value is unique in the file, if so return it, else try again
    def Generate_Salt(self, fileName):
        import csv
        while True:
            try:
                from random import randrange
                from sys import maxsize
                salt = randrange(maxsize)
                with open(fileName, 'rt') as file:
                    reader = csv.reader(file, delimiter=",")
                    for row in reader:
                        if salt == row[1]: continue
            except IndexError:
                return salt
            return salt
    
############################################################################### 
    # Validates that the user can use the provided user ID
    def Check_Credential(self, credential, fileName):
        import csv        
        try:
            with open(fileName, 'rt') as file:
                reader = csv.reader(file, delimiter=",")
                for row in reader:
                    if credential == row[0]: return True
                    
        # The credential was not found in the file, allow with user signup
        except IndexError: 
            return False
        return False
    
############################################################################### 
    # Validates that the 
    def Authenticate_User(self, userID, password, fileName):
        import hashlib
        import csv        
        try:
            with open(fileName, 'rt') as file:
                #reader = file.read().split('\n')
                reader = csv.reader(file, delimiter=",")
                for row in reader:
                    #print(row)
                    if userID == row[0]:
                        salt = row[1]
                        hashValue = (str(salt) + password).encode()
                        hashValue = hashlib.sha256(hashValue)
                        hashValue = hashValue.hexdigest()
                        
                        if hashValue == row[2]: return True
                        else: False
                    
        # There are no users in the file, allow the user ID to continue
        except IndexError: 
            return False
        return False