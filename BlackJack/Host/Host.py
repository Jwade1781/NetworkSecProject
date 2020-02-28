###############################################################################
# Current orders of operations:
# [1] Generate a Public / Private Key Pair
# [2] Listen for any attempted client connections
# [3] Send Connected Client the generated public host key (Unencrypted)
# [4] Receive the generated encrypted symmetric key from client (Decrypt hosts privateKey)
#
# [5] Ask User what they want to do: (Encrypt AES128)
#       A. Login
#       B. Signup
#
# [5.A] A. Ask User to input UserID (Encrypt AES128)
#       B. Receive UserID (Decrypt AES128)
#       C. Ask User to input Password (Encrypt AES128)
#       D. Receive Password (Decrypt AES128)
#       E. Open password file and look for any matching userID's
#           [Success] Pull row (userID, salt, hash)
#                     Append salt with inputted password and generate a hash value
#                     if generated hash and the hash in file do not match, go to [unsuccess]
#                     else go to step [6]
#
#           [Unsuccess] Tell client that login was unsuccessful
#                       Raise amounts of attempts tried
#                       if maxed attempts are reached, close connection
#                       Else repeat step [5.A]
#
# [5.B] A. Ask User for the User ID, retrieve and decrypt
#       B. Open password file and make sure UserID is not currently in use .. Send [1] if good to use or [0] if the userID is already in use
#       C. Ask User for the password, retrieve and decrypt
#       D. Generate random salt value that is not already in use in the password file
#       E. Hash the inputted password with the unique Salt value
#       F. Store the userID, salt, and generated hash value in password file
#
# [6] Start blackjack game will update later with operations

###############################################################################
class Host:
    def __init__(self):        
        # [1]
        self.hostPublicKey, self.hostPrivateKey = self.Generate_Host_Keys()
        print("Generated Keys:")
        print("Public:\n", self.hostPublicKey)
        print("\n\nPrivate:\n", self.hostPrivateKey)
        self.connection_pool = []
        self.connections = []
        self.Start_Connection_Thread()
            
        print("All Connections Closed")

###############################################################################        
    # Generates a random key based on the number of bytes needed
    def Generate_AES_Key(self, KEYSIZE):
        import os
        return os.urandom(KEYSIZE)
    
###############################################################################
    def Start_Connection_Thread(self):
        import threading
        import os
        #mainThreadPid = os.getpid()
        #for threadCount in range (0, THREADS):
        
        #connectionThread = threading.Thread(target=self.Listen_For_Connection)
        #connectionThread.start()
        self.Listen_For_Connection(0)
        #print("Connection Thread Terminated")
        
###############################################################################
    def Listen_For_Connection(self, threadNumber):
        while(True):
            try:
                import socket
                newSocket = socket.socket()
                host = socket.gethostname()
                port = 12371 + threadNumber
                newSocket.bind((host, port))
            except:
                port +=1
                continue
        
            print('Listening to port:', port)
            MAX_LISTNENING_QUEUE = 1
            
            #[2] Wait for a new client connection
            newSocket.listen(MAX_LISTNENING_QUEUE)
            self.Add_New_Connection(newSocket)
            
            #[3] Send host public Key to the client (e, n values)
            self.communication.Send_Message(0, str(self.hostPublicKey[0]), False)
            self.communication.Send_Message(0, str(self.hostPublicKey[1]), False)
            
            
            #[4] Receive Client info: their public key, username, and password
            self.AES_Secret_Key = self.communication.Receive_Message(self.hostPrivateKey, False) #Not encrypting/decrypting yet until RSA keys work
            #print("Received Secret Key:", self.AES_Secret_Key)

            #[5] Ask user for what they would like to do.. signup or login
            message = "What would you like to do?\n[1] Login\n[2] Signup"
            self.communication.Send_Message(0, message, False)

            response = self.communication.Receive_Message(self.AES_Secret_Key, False) #Not encryted yet

            # [5.A] User inputted 1; would like to login
            if (str(response) == '1'):
                while (self.attempts > 0):
                    if (User_Login()):
                        print("Login Successful")
                        self.communication.Send_Message(self.AES_Secret_Key, 'Login was successful', False) 
                        break

                    else:
                        self.attempts -= 1
                        self.communication.Send_Message(self.AES_Secret_Key, 'Login was unsuccessful', False)
                        if (self.attempts == 0):
                            self.connection.close() # Ran out of attempts close connection
                    

            # [5.B] User inputted 2; would like to signup
            elif (str(response) == '2'):
                New_User_Signup()
            
            #[6]
            #Play_Black_Jack()
###############################################################################
    def Add_New_Connection(self, socket):
        from Communication import Communication
        
        self.connection, self.address = socket.accept()
        self.communication = Communication(self.connection)       
        self.connections.append(self.address)
        self.connection_pool.append(self.connection)
        print("Connection established with", self.address,'\nTotal Connections:', len(self.connection_pool))
        
###############################################################################
    def Generate_Host_Keys(self):
        from RSA import RSA
        RSA = RSA()
        return RSA.Generate_Key_Pair()
        
###############################################################################
    def User_Login(self):
        self.communication.Send_Message(self.AES_Secret_Key, 'Enter your userID', False)
        userID = self.communication.Receive_Message(self.AES_Secret_Key, False)
        self.communication.Send_Message(self.AES_Secret_Key, 'Enter your password', False)
        password = self.communication.Receive_Message(self.AES_Secret_Key, False)
        # Check to see if the username was in the password file, will return False if it was
        if (not self.Check_Password_File(userID), 0):
            salt, _hash = self.Pull_Password_File_Row(userID)
            generatedHash = hash(str(salt) + password)
            if (generatedHash == _hash):
                return True # User was able to login
        
        # User was unable to login either from invalid username or password
        return False

###############################################################################
    def New_User_Signup(self):
        message = 'Enter the UserID that you would like to use'
        self.communication.Send_Message(0, message, False)
        validUserID = False

        while(not validUserID):
            userID = self.communication.Receive_Message(self.AES_Secret_Key, False)
            validUserID = Check_Password_File(userID, 0)
            if (not validUserID):
                self.communication.Send_Message(self.AES_Secret_Key, "User ID already in use.. pick another", False)

        # Generate valid unique salt value
        validSalt = False
        while(not validSalt):
            # Create a random unique salt value
            import random, base64, struct
            randomValue = random.SystemRandom().random()
            salt = base64.b64encode((struct.pack('id', randomValue)))# 12 char salt value
            validSalt = Check_Password_File(salt, 1)

        
        self.communication.Send_Message(self.AES_Secret_Key, 'Enter the password that you would like to use', False)
        password = self.communication.Receive_Message(self.AES_Secret_Key, False)

        # Generate a hash given the inputted password and generated salt value
        hashValue = hash(str(salt) + password)
        print(hashValue)

        # Dump the userID, Salt value, and hash into passwordFile.csv
        
###############################################################################
    def Check_Password_File(self, itemSearched, elementPlacement):
        PASSWORD_FILE = 'passwordFile.csv'
        import csv
        with open('passwordFile.csv') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            for row in csv:
                if (row[elementPlacement] == itemSearched):
                    return False # Element was found in password file
            return True # element not found in password file

###############################################################################
    def Pull_Password_File_Row(self, userID):
        PASSWORD_FILE = 'passwordFile.csv'
        import csv
        with open('passwordFile.csv') as csvFile:
            csvReader = csv.reader(csvFile, delimiter=',')
            for row in csv:
                if (row[0] == userID):
                    salt = row[1]
                    _hash = row[2]
                    return salt, _hash