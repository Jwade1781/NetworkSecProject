##############################################################################
class Encrypt:
    # On startup generate both the AES key and a RSA key pair
    #def __init__(self):
        #KEYSIZE = 16
        #self.aesKey = self.Generate_AES_Key(KEYSIZE)
  
    #    KEYSIZE = 2048
    #    self.publicKey, self.privateKey = self.Generate_RSA_Key_Pair(KEYSIZE)

##############################################################################
    def Encrypt_Message_AES(self, plainText, KEYSIZE):
        BLOCKSIZE_BYTES = 16
        plainText = self.Pad_Message_AES(plainText, BLOCKSIZE_BYTES)
        
        # Create the IV
        import os
        self.iv = os.urandom(KEYSIZE)
        print("IV: ", str(self.iv))
        
        from Crypto.Cipher import AES
        aes = AES.new(self.aesKey, AES.MODE_CBC, self.iv)
        cipherText = aes.encrypt(plainText)
        return cipherText
    
##############################################################################
    # Pad the message such that the message's byte length is a multiple of 16
    # Each padding holds the value of the total number of padding needed
    def Pad_Message_AES(self, plainText, BLOCKSIZE_BYTES):
        paddedPlainText = bytes(str(plainText), encoding='utf8')
        length = BLOCKSIZE_BYTES - (len(plainText) % BLOCKSIZE_BYTES)
        paddedPlainText += (bytes([length])*length)
        return paddedPlainText
    
##############################################################################
    def Encrypt_Message_RSA(self, publicKey, plainText):
        import rsa
        #plainText = plainText.encode('utf8')
        cipherText = rsa.encrypt(plainText, publicKey, n=2048)
        return cipherText

##############################################################################        
    def Generate_RSA_Key_Pair(self, KEYSIZE):
        import rsa
        publicKey, privateKey = rsa.newkeys(KEYSIZE)
        return publicKey, privateKey

##############################################################################
    # The IV is not treated as a key so it can be sent directly to the client
    # in plaintext
    def Get_IV(self):
        return self.iv
    
##############################################################################
    def Get_Cipher(self):
        return self.cipherText
    
##############################################################################
    def Get_Key_Pair(self):
        return self.publicKey, self.privateKey