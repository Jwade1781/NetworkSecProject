class Communication:
    def __init__(self, connection):
        self.connection = connection
        
###############################################################################
    def Receive_Message(self, key, encryptionNeeded):            
        BUFFER_SIZE = 4096
        messageLength = self.connection.recv(BUFFER_SIZE)
        messageLength = int(messageLength.decode())
        receivedMessage = []
        
        for i in range (0, messageLength):
            message = self.connection.recv(BUFFER_SIZE)
            receivedMessage.append(message.decode())
            
        if (encryptionNeeded == True):
            from RSA import RSA
            RSA = RSA()
            # Decrypt the received Message here 
            # PLACEHOLDER
            receivedMessage = RSA.Decrypt(key, receivedMessage)
        
        
        # Return the appropriate response; 
        # if it can be a boolean return a bool, else return string
        #if (receivedMessage.lower() == 'false'):
        #    return False
        
        #elif (receivedMessage.lower() == 'true'):
        #    return True
        
        print("Received Message:")
        print(receivedMessage, end='\n\n')
        return(receivedMessage)
        
        
###############################################################################
    def Send_Message(self, key, message, encryptionNeeded):        
        if (encryptionNeeded == True):
            from RSA import RSA
            # Encrypt the sending Message here with provided public key from host
            # PLACEHOLDER
            print("Encrypting with key:")
            print(key, end='\n\n')
            RSA = RSA()
            message = RSA.Encrypt(key, str(message))
            print("Encrypted message:")
            print(message, end="\n\n")
        
        # tells how many chars to expect
        messageLength = str(len(message))
        self.connection.send(messageLength.encode())
        print("Sent length:", messageLength)
        
        # Send the message to the host here
        self.connection.send(message.encode())
        print("Sent message:", message)