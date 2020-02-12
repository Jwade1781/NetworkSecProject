class Card:    
    def __init__(self, suit, cardVal):
        self.suit = suit
        self.cardVal = str(cardVal)
        self.cardID = (self.suit + self.cardVal).lower() #ID of the card used for identifying which card pic to display
        
    def GetSuit(self):
        return self.suit
    
    def GetCardVal(self):
        return self.cardVal
    
    def GetCardId(self):
        return self.cardID
    
    def PrintCard(self):
        print('[' + self.suit +']', end='')
        
        paddedSpaces = 15 - len(self.suit) 
        for i in range (0, paddedSpaces):
            print(' ', end='')
            
        print('[' + self.cardVal + ']')