# Order of operations for black jack (host)
# [1] Load the number of credits that the user has and send to client the amount
# [2]
class BlackJack:
    def __init__(self, communication, userID, clientPublicKey, hostPrivateKey):
        userCredits = self.Get_User_Credits(userID)
        deck = self.Generate_Deck(3)
        playing = True
        try:
            while playing:
                communication.Send_Message(True, "RSA", clientPublicKey, userCredits)
                playing, userCredits = self.Play_Game(communication, userCredits, clientPublicKey, hostPrivateKey, deck)
        except:
            print("Terminated Connection")
        
        
        # Update the number of credits the user has finished with
        self.Update_User_Credits(userID, userCredits)
        
        #print(userID, userCredits)
    
###############################################################################
#   Goes through the Credits file and looks for the matching userID, returns the
#   credits that correspond with the userID
    def Get_User_Credits(self, userID):
        CREDITSFILE = "host/Credits.csv"
        import csv
        try:
            with open(CREDITSFILE, 'rt') as file:
                #reader = file.read().split('\n')
                reader = csv.reader(file, delimiter=",")
                for row in reader:
                    if userID == row[0]: return row[1]
                    
        # There are no users in the file, allow the user ID to continue
        except IndexError: 
            return None
        return None

###############################################################################
#   Updates the amount the user has based upon what was bet
    def Update_User_Credits(self, userID, userCredits):
        CREDITSFILE = "host/Credits.csv"
        import csv
        newRowVal = [userID, userCredits]
        try:
            rows = []
            with open(CREDITSFILE, "r") as file:
                reader = csv.reader(file, delimiter=",")
                for row in reader:
                    if row[0] == userID:
                        row = newRowVal
                    rows.append(row)
                    
            with open(CREDITSFILE, 'w') as file:
                writer = csv.writer(file, delimiter=",")
                for row in rows:
                    writer.writerow(row)
                    
        # There are no users in the file, allow the user ID to continue
        except IndexError: 
            return 
        return 
    
###############################################################################
    def Generate_Deck(self, deckSize):
        from Generate_Deck import Deck
        cards = Deck(deckSize)
        return cards
    
###############################################################################
    def Play_Game(self, communication, userCredits, clientPublicKey, hostPrivateKey, deck):
        betAmount = self.Place_Bet_Amount(communication, userCredits, clientPublicKey, hostPrivateKey)
        cards = self.Generate_Deck(3)
        userCard = self.Draw_Card(communication, clientPublicKey, cards, "User")
        hostCard = self.Draw_Card(communication, clientPublicKey, cards, "Host")
        communication.Receive_Message(True, "RSA", hostPrivateKey)
        userCredits = int(userCredits)
        if userCard.GetCardVal() < hostCard.GetCardVal(): 
            message = "You lose\n"
            userCredits -= int(betAmount)
        elif userCard.GetCardVal() > hostCard.GetCardVal(): 
            message = "You Win\n"
            userCredits += int(betAmount)
        else: message = "You have tied\n"
        message += "Would you like to play again?\n[1] Yes\n[2] No\n"
        communication.Send_Message(True, "RSA", clientPublicKey, message)
        playAgain = communication.Receive_Message(True, "RSA", hostPrivateKey)
        if playAgain == "1": return True, str(userCredits)
        else: return False, str(userCredits)
        
###############################################################################
    def Draw_Card(self, communication, clientPublicKey, cards, playerType):
        card = cards.Draw_Card()
        message = playerType + " has drawn " + card.GetSuit() + " " + card.GetCardVal() + " "
        communication.Send_Message(True, "RSA", clientPublicKey, message)
        return card
                
###############################################################################       
        
# Ask client how much they would like to bet and retrieve response
    def Place_Bet_Amount(self, communication, userCredits, clientPublicKey, hostPrivateKey):
        validBet = False
        while not validBet:
            message = "How much would you like to bet? Enter an integer dollar amount\n"
            communication.Send_Message(True, "RSA", clientPublicKey, message)
            betAmount = communication.Receive_Message(True, "RSA", hostPrivateKey)
            
            if int(betAmount) <= int(userCredits): 
                communication.Send_Message(True, "RSA", clientPublicKey, "True")
                return betAmount
            
            else: 
                communication.Send_Message(True, "RSA", clientPublicKey, "You have entered an invalid bet.. Please try again\n")
                communication.Receive_Message(True, "RSA", hostPrivateKey)