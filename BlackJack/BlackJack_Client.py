# Order of operations for black jack
# [1] Receive the number of credits that the client currently has
# [2] 
class BlackJack:
    def __init__(self, communication, hostPublicKey, clientPrivateKey):
        playing = True
        while playing:
            print("================== Starting Black Jack Game ===================")
            userCredits = communication.Receive_Message(True, "RSA", clientPrivateKey)
            print("\nCurrent Credits: ", userCredits)
            playing = self.Play_Game(communication, userCredits, hostPublicKey, clientPrivateKey)
            
        communication.Close_Connection()
        # Update the number of credits the user has finished with
        #print(userID, userCredits)
    
###############################################################################
    def Play_Game(self, communication, userCredits, hostPublicKey, clientPrivateKey):
        # Ask the user how much they would like to bet and return it
        betAmount = self.Place_Bet_Amount(communication, hostPublicKey, clientPrivateKey, userCredits)
        print("\nYou have placed a bet amount of", betAmount)        
        userCard = communication.Receive_Message(True, "RSA", clientPrivateKey)
        print(userCard)
        hostCard = communication.Receive_Message(True, "RSA", clientPrivateKey)
        print(hostCard)
        communication.Send_Message(True, "RSA", hostPublicKey, "Ack")
        outcome = communication.Receive_Message(True, "RSA", clientPrivateKey)
        playAgain = ""
        while playAgain != "1" and playAgain != "2": playAgain = input(outcome)
        
        communication.Send_Message(True, "RSA", hostPublicKey, playAgain)  
        if playAgain == "1": return True
        else: return False
        
        #cards.Print_All_Cards()

###############################################################################        
# Ask client how much they would like to bet and retrieve response
    def Place_Bet_Amount(self, communication, hostPublicKey, clientPrivateKey, userCredits):
        validBet = False
        while not validBet:
            betAmount = ""
            message = communication.Receive_Message(True, "RSA", clientPrivateKey)
                
            while not betAmount.isdigit():
                betAmount = input(message)
            
            communication.Send_Message(True, "RSA", hostPublicKey, betAmount)
            strValidBet = communication.Receive_Message(True, "RSA", clientPrivateKey)
            if strValidBet == "True": return betAmount
            else: 
                communication.Send_Message(True, "RSA", hostPublicKey, "Ack")
                print(strValidBet)
            