##############################################################################
class Decrypt:
    #def __init__(self, method, key, KEYSIZE, cipherText, iv):
        #if (method == 'AES'):
        #    self.plainText = self.Decrypt_Message_AES(key, cipherText, KEYSIZE, iv)
            
        #elif (method == 'RSA'):
        #    self.plainText = self.Decrypt_Message_RSA(key, cipherText)

##############################################################################
    def Decrypt_Message_AES(self, key, cipherText, KEYSIZE, iv):
        BLOCKSIZE_BYTES = 16
        #plainText = self.Pad_Message(plainText, BLOCKSIZE_BYTES)
        
        iv = self.Pad_IV(iv, BLOCKSIZE_BYTES)
        
        from Crypto.Cipher import AES
        print("Not here")
        plainText = AES.new(bytes(str(key), encoding='utf8'), AES.MODE_CBC, (bytes(str(iv), encoding='utf8')))
        print("Here")
        #plainText = Depad_Message()
        return plainText
    
##############################################################################
    def Decrypt_Message_RSA(self, privateKey, cipherText):
        import rsa
        plainText = rsa.decrypt(cipherText, privateKey)
        message = plainText.decode('utf8')
        print("Decrypted Message:", message)
        return message
    
##############################################################################
    # Pad the message such that the message's byte length is a multiple of 16
    # Each padding holds the value of the total number of padding needed
    def Pad_IV(self, iv, BLOCKSIZE_BYTES):
        paddedIV = bytes(str(iv), encoding='utf8')
        length = BLOCKSIZE_BYTES - (len(iv) % BLOCKSIZE_BYTES)
        paddedIV += (bytes([length])*length)
        return paddedIV
    
##############################################################################
    # Pad the message such that the message's byte length is a multiple of 16
    # Each padding holds the value of the total number of padding needed
    def Depad_Message(self, plainText, BLOCKSIZE_BYTES):
        paddedPlainText = bytes(str(plainText), encoding='utf8')
        length = BLOCKSIZE_BYTES - (len(plainText) % BLOCKSIZE_BYTES)
        paddedPlainText += (bytes([length])*length)
        return paddedPlainText

##############################################################################
    def Get_Plain(self):
        return self.plainText
    
##############################################################################