class Encryption:        
###############################################################################
    def Generate_RSA_Keys(self, keySize, exponent):
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.serialization import(
            Encoding, PublicFormat, PrivateFormat, NoEncryption
        )
        self.private_key = rsa.generate_private_key(
            public_exponent=exponent,
            key_size=keySize,
            backend=default_backend()
        )
        privateKey = self.private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption())
        publicKey = self.private_key.public_key().public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
        return privateKey.decode("utf-8"), publicKey.decode("utf-8")
    
###############################################################################
    def Encrypt_Message(self, key, message):
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding
            
        cipherText = key.encrypt(
            str.encode(message),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return cipherText

###############################################################################
    def Decrypt_Message(self, key, cipherText):
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding
                
        plainText = key.decrypt(
            cipherText,
            padding.OAEP(
                mgf = padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plainText
    
###############################################################################