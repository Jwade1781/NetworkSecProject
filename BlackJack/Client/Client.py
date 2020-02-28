###############################################################################
# Current orders of operations:
# [1] Establish Connection with Host
# [2] Receive the hosts public key (No Encryption needed)
# [3] Generate an AES128 Secret Key
# [4] Send the AES128 Secret Key to host (Encrypt Host's publicKey)
# [5] Receive prompt of what the client would like to do (Decrypt AES128)
# [6] Send Response to Host with request (Encrypt AES128)
#       A. Login
#       B. Signup
#
# [6.A] A. Receive Login userID prompt and send userID (Decrypt AES128 / Encrypt AES128)
#       B. Receive Login password prompt and send password (Decrypt AES128 / Encrypt AES 128)
#
# [6.B] A. Receive Prompt to enter userID and send the inputted userID (Decrypt AES128 / Encrypt AES128)
#       B. Receive prompt on either enter a password or the userID is already in use (Decrypt AES128)
#          If in use repeat second half of step A
#       C. If not in use, input the desired password, validate it is at least 8 chars in length
#       D. Send Password to Host (Encrypt AES128)
#
# [7] Start blackjack game

###############################################################################
class Client:
    def __init__(self):
        # [1] Establish connection with host
        from Communication import Communication
        self.communication = Communication(self.Establish_Connection())
        
        # [2] Receive hosts public key (e, n values)
        e = (self.communication.Receive_Message(0, False))
        n = (self.communication.Receive_Message(0, False))
        hostPublicKey = [e, n]
        print("Received host public key:\n", hostPublicKey, end='\n\n')
        
        # [3] Generate AES128 Secret Key
        self.AES_Secret_Key = self.Generate_AES_Key()
        #self.AES_Secret_Key = 123

        
        # [4] Encrypt the secret key with the public key and send to host
        self.communication.Send_Message(hostPublicKey, self.AES_Secret_Key, False)
        
        # [5] Receive Prompt
        print(self.communication.Receive_Message(self.AES_Secret_Key, False))
        response = ''
        while (response != '1' or response != '2'):
            response = input()

        # Send response to host
        self.communication.Send_Message(self.AES_Secret_Key, response, False)
        loggedIn = False
        if (response == '1'):
            while (not loggedIn):
                loggedIn = self.Client_Login()
        
        elif (response == '2'):
            self.Client_Signup()
        
###############################################################################        
    def Establish_Connection(self):
        import socket
        connection = socket.socket()
        host = socket.gethostname()
        port = 12371
        while(True):
            try:
                print('Connecting to port:', port)
                connection.connect((host, port))
                break
            except:
                print("Connection failed")
                port += 1
                continue
            
        return connection

###############################################################################     
    def Generate_AES_Key(self):
        from base64 import b64encode
        from os import urandom
        random = urandom(64)
        return b64encode(random).decode('utf-8')

############################################################################### 
    def Client_Login(self):
        print(self.communication.Receive_Message(self.AES_Secret_Key, False))
        userID = input()
        self.communication.Send_Message(self.AES_Secret_Key, userID, False)
        print(self.communication.Receive_Message(self.AES_Secret_Key, False))
        password = input()
        self.communication.Send_Message(self.AES_Secret_Key, password, False)
        hostResponse = self.communication.Receive_Message(self.AES_Secret_Key, False)
        print (hostResponse)
        if (hostResponse == "Login Successful"):
            return True
        else:
            return False

############################################################################### 
    def Client_Signup(self):
        print(self.communication.Receive_Message(self.AES_Secret_Key, False))
        validUserID = False
        while (not validUserID):
            userID = input()
            self.communication.Send_Message(self.AES_Secret_Key, userID, False)

            hostResponse = self.communication.Receive_Message(self.AES_Secret_Key, False)
            if (hostResponse == "User ID already in use.. pick another"):
                validUserID = True
        
        password =''
        print(self.communication.Receive_Message(self.AES_Secret_Key, False))
        while (len(password) < 8):
            password = input()
        self.communication.Send_Message(self.AES_Secret_Key, password, False)