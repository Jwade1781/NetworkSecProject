# -*- coding: utf-8 -*-
class Communication:
    def __init__(self, connection):
        self.connection = connection
        
###############################################################################
# Receive message from the other side of the connection
# if it was encrypted, decrypt it with the provided key
    def Receive_Message(self, encryptionNeeded, encryptionAlgorithm, key):
        BUFFER_SIZE = 2048
        receivedMessage = self.connection.recv(BUFFER_SIZE)
        if (encryptionNeeded == True):
            from Encryption import Encryption
            receivedMessage = Encryption().Decrypt_Message(key, receivedMessage[:512])
        
        receivedMessage = receivedMessage.decode()
        #print("Received message:", receivedMessage)
        return(receivedMessage)

###############################################################################
# Send the message to the client attempt to encode it into a byte object if it hasn't been already
# If encryption is needed, encrypt with the provided key object
    def Send_Message(self, encryptionNeeded, encryptionAlgorithm, key, message):
        if encryptionNeeded==True:
            from Encryption import Encryption
            message = Encryption.Encrypt_Message(self, key, message)
        try:
            self.connection.send(message.encode())
        except:
            self.connection.send(message)
        #print("Sent message:", message)
    
###############################################################################
    def Close_Connection(self):
        self.connection.close()
        print("Connection was closed\n")
            
    