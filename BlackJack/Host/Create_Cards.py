
def main():
    DECKSIZE = 1
    cards = CreateDeck(DECKSIZE)
    cards = ShuffleCards(cards)
    
    PrintAllCards(cards)
        
def CreateDeck(DECKSIZE):
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

def ShuffleCards(cards):
    from random import shuffle, uniform, seed, randint
    from time import sleep
    
    MINSHUFFLE = 1000
    MAXSHUFFLE = 3500
    SHUFFLETIMES = randint(MINSHUFFLE, MAXSHUFFLE)
    total = 0
    for i in range (0, SHUFFLETIMES):  
        seed(uniform(0.00, 1000))
        shuffle(cards)
        
        timeSleep = uniform(0.00, 0.009)
        sleep(timeSleep)
        total += timeSleep
        
    print("Total:", total, "\t Times shuffled:", SHUFFLETIMES)
    return cards

def PrintAllCards(cards):
    i = 0
    for i in range (0, len(cards)):
        cards[i].PrintCard()
        
    print("TOTAL CARDS:",i)

main()