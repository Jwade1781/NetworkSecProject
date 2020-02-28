###############################################################################
class RSA:
    def Generate_Key_Pair(self):
        d = 0
        # Loop until valid p q pairs are generated that can be used
        while (d == 0):       
            p, q = self.Generate_Prime_Pair("first_100k_primes.csv")
            # n -> attach to both keys
            n = p * q
            
            # phi(N) -> used to calculate e and d
            phi = (p - 1) * (q - 1)
            
            # e -> attach to public key
            e = 5
            
            d = self.Find_D(e, phi)
            if d == e:
                continue

        publicKey = [e, n]
        privateKey = [d, n]
        
        #print("Generated Values:")
        #print("p:", p, "q:", q, 'n:', n)
        #print("phi:", phi, "e:", e, "d:", d)
        return publicKey, privateKey

###############################################################################  
    def Generate_Prime_Pair(self, FILENAME):
        import csv
        from random import randrange
        qValue = 0
        pValue = 0
        
        while(qValue == 0 or pValue == 0 or pValue == qValue):
            TOTAL_PRIMES = 100
            pRandom = randrange(TOTAL_PRIMES)
            qRandom = randrange(TOTAL_PRIMES)
            
            # Loop through the file's rows, setting values of p and q after their
            # allocated random passes is reached
            passedPrimes = 0
            
            with open(FILENAME) as primeFile:
                csvReader = csv.reader(primeFile, delimiter=',')
                for row in csvReader:                
                    if passedPrimes == pRandom:
                        pValue = row
                    elif passedPrimes == qRandom:
                        qValue = row
                    passedPrimes +=1
            try: 
                qValue = int(qValue[0])
                pValue = int(pValue[0])
                break
            except:
                continue
        return pValue, qValue      
        
        
###############################################################################        
    def Find_D(self, e, phi):
        g, x, y = self.Extended_Greatest_Common_Divisor(e, phi)
        if g != 1:
            #raise Exception("Inverse does not exist")
            return 0
        return x % phi
    
    def Extended_Greatest_Common_Divisor(self, e, phi):
        if (e == 0):
            return (phi, 0, 1)
        else:
            g, y, x = self.Extended_Greatest_Common_Divisor(phi % e, e)
            return (g, x - (phi // e) * y, y)

###############################################################################    
    def Encrypt(self, publicKey, plainText):
        print("Given:", publicKey)
        #publicKey = publicKey.replace("[", "")
        #publicKey = publicKey.replace("]", "")
        #end = publicKey.find(',')
        #e = int(publicKey[:end])
        #n = int(publicKey[end+2:])
        e = int(publicKey[0])
        n = int(publicKey[1])

        cipherText = []
        for char in plainText:
            cipherText.append((ord(char) ** e) % n)

        #print("\nCipherText:", cipherText, end='\n\n')
        return cipherText
    
    
        #cipherText = ''
        #for char in plainText:
        #    cipherText += str(((ord(char) ** e) % n))

        #print("\nCipherText:", cipherText, end='\n\n')
        #print("Cipher Text:", cipherText)
        #return cipherText
        
###############################################################################
    def Decrypt(self, privateKey, cipherText):
        print("Given:", privateKey)
        #cipherText = str(cipherText)
        #privateKey = privateKey.replace("[", "")
        #privateKey = privateKey.replace("]", "")
        #end = privateKey.find(',')
        
        d = int(privateKey[0])
        n = int(privateKey[1])
        
        #d = int(privateKey[:end])
        #n = int(privateKey[end+2:])
        plainText = ''

        for char in cipherText:
            print("char:", char)
            print("n:", n)
            print("d:", d)
            #temp = (int(char) ** d) % n
            plainText += (chr((int(char) ** d) % n))
            #print("temp:", temp)
            #plainText += chr(temp)
            #print(plainText)
        return plainText
    
###############################################################################