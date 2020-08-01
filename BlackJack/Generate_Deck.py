class Deck:
###############################################################################
    def __init__(self, deckSize):
        self.DECKSIZE = deckSize
        self.cards = self.Shuffle_Cards()

###############################################################################        
    def Create_Deck(self, DECKSIZE):
        from Card import Card
        cards = []
        suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        faceCards = ['Jack', 'Queen', 'King', 'Ace']
        for i in range (0, DECKSIZE):
        
            # Create a new deck by iterating through all card values and the suits
            for createSuit in range (0, len(suits)):
            
                # Add all none face cards to deck
                for cardVal in range (2, 11):
                    newCard = Card(suits[createSuit], cardVal)
                    cards.append(newCard)
                    
            # Add all face cards to deck
                for cardVal in range(0, len(faceCards)):
                    newCard = Card(suits[createSuit], faceCards[cardVal])
                    cards.append(newCard)
        
        # Attach a reshuffle card that will be used to reshuffle the deck once it is drawn
        # Helps prevent the predictablility of cards towards the end of the deck
        newCard = Card('Reshuffle', 'Void')
        cards.append(newCard)
        return cards

###############################################################################
    def Shuffle_Cards(self):
        from random import shuffle, uniform, seed, randint
        from time import sleep
        self.cards = self.Create_Deck(self.DECKSIZE)
        
        MINSHUFFLE = 50
        MAXSHUFFLE = 75
        SHUFFLETIMES = randint(MINSHUFFLE, MAXSHUFFLE)
        total = 0
        for i in range (0, SHUFFLETIMES):  
            seed(uniform(0.00, 1000))
            shuffle(self.cards)
        
            timeSleep = uniform(0.00, 0.009)
            sleep(timeSleep)
            total += timeSleep
        
        #print("Total:", total, "\t Times shuffled:", SHUFFLETIMES)
        return self.cards

###############################################################################
    def Print_All_Cards(self):
        i = 0
        for i in range (0, len(self.cards)):
            self.cards[i].PrintCard()
        
        print("TOTAL CARDS:",i)
        
###############################################################################
    def Draw_Card(self):
        while True:
            card = self.cards.pop(0)
            if (card.GetSuit() == 'Reshuffle'): self.Shuffle_Cards()
            else: return card

###############################################################################