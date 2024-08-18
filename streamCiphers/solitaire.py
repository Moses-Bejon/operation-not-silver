import string

class solitaire:
    jokerA = 53
    jokerB = 54

    def __init__(self,deckConfig):
        self.deckConfig = deckConfig
        self.keyedDeck = [self.cardToVal(card) for card in deckConfig]

    def letterToNum(self, letter):
        return string.ascii_uppercase.index(letter) + 1

    def numToLetter(self, number):
        return string.ascii_uppercase[(number - 1) % 26]

    # convert deck of cards to numbers
    def cardToVal(self, card):
        suits = {
            '♣': (1, 13),
            '♦': (14, 26),
            '♥': (27, 39),
            '♠': (40, 52)
        }

        if card == 'joker A':
            return self.jokerA
        if card == 'joker B':
            return self.jokerB

        suit = card[-1]
        rank = card[:-1]

        if rank == 'A':
            rank = 1
        elif rank == 'J':
            rank = 11
        elif rank == 'Q':
            rank = 12
        elif rank == 'K':
            rank = 13
        else:
            rank = int(rank)

        val, _ = suits[suit]
        return val + rank-1

    def moveJokerA(self, deck):
        # If jokerA on bottom, put it just after the top card, else swap joker A with card below it
        if deck[-1] == self.jokerA:
            deck.insert(1, deck.pop())
        else:
            index = deck.index(self.jokerA)
            deck[index], deck[index+1] = deck[index+1], deck[index]

    def moveJokerB(self, deck):
        # If joker B is on the bottom of the deck, put it just after the second card.
        # If joker B is the second to-last card, put it just after the top card.
        # If neither of these is the case, move joker B down by two cards.
        if deck[-1] == self.jokerB:
            if len(deck) > 2:
                deck.insert(2, deck.pop())
            else:
                deck.insert(1, deck.pop())
        elif deck[-2] == self.jokerB:
            deck.insert(1, deck.pop())
        else:
            index = deck.index(self.jokerB)
            deck.insert((index + 2) % len(deck), deck.pop(index))

    # triple cut - swap stack of cards above 1st joker with stack of cards below 2nd joker
    # 1st joker = joker close to the top
    def tripleCut(self, deck):
        firstJoker = min(deck.index(self.jokerA), deck.index(self.jokerB))
        secondJoker = max(deck.index(self.jokerA), deck.index(self.jokerB))
        deck = deck[secondJoker + 1:] + deck[firstJoker:secondJoker + 1] + deck[:firstJoker]
        return deck

    # count cut -  Look at the bottom card. If it is a joker, do nothing for this step.
    # Else - take the number corresponding to that card and do a count cut by taking a stack of that many card off the top of the deck and putting that stack just above the bottom card.

    def countCut(self, deck):
        bottomVal = self.cardVal(deck[-1])
        if bottomVal in [self.jokerA, self.jokerB]:
            return deck
        deck = deck[bottomVal:-1] + deck[:bottomVal] + [deck[-1]]
        return deck

    # # Convert the letter of the keyword to a number, where ‘A’ = 1, ‘B’ = 2, ‘C’ = 3, ..., ‘Z’ = 26
    # # do another count cut by taking a stack of that many card off the top of the deck and putting that stack just above the bottom card.
    # def addCountCut(self, deck, letter):
    #     countVal = self.letterToNum(letter)
    #     deck = deck[countVal - 1:] + deck[:countVal - 1] + [deck[-1]]
    #     return deck

    def cardVal(self, card):
        if card == self.jokerA or card == self.jokerB:
            return 53
        return card

    # generate keystream
    def generateKeystreamVal(self, deck):
        while True:
            self.moveJokerA(deck)
            self.moveJokerB(deck)
            deck = self.tripleCut(deck)
            deck = self.countCut(deck)

            topVal = deck[0]
            if topVal in [self.jokerA, self.jokerB]:
                continue

            # Take stack of topVal cards off deck
            stack = deck[1:topVal + 1]
            remainingDeck = deck[topVal + 1:]

            # New top card after stack 
            newTopVal = remainingDeck[0]
            # Put stack back on top of deck
            deck = stack + remainingDeck

            # if newTopVal = 53, repeat from step 1
            if newTopVal == 53:
                continue
            elif newTopVal > 26:
                newTopVal -= 26

            return newTopVal

    # generate required length of keystream
    def generateKeystream(self, deck, length):
        keystream = []
        for _ in range(length):
            keystream.append(self.generateKeystreamVal(deck))
        return keystream

    def decipher(self, cipherText, deck):
        keystream = self.generateKeystream(deck.copy(), len(cipherText))
        print(f'Keystream: {keystream}')
        print(deck)

        plainText = []
        for i, letter in enumerate(cipherText):
            cipherVal = self.letterToNum(letter)
            keyVal = keystream[i] % 26
            plainVal = (cipherVal - keyVal - 1) % 26
            if plainVal == 0:
                plainVal = 26
            plainText.append(self.numToLetter(plainVal))

        return ''.join(plainText)


deckConfig = [
    '5♦', '6♦', '7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦',
    '9♣', 'joker A', '7♣', '5♣', 'J♣', 'Q♣', 'J♥', 'Q♥', 'joker B',
    'A♥', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥',
    '10♣', 'K♥', 'A♠', '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠',
    '9♠', '10♠', 'J♠', 'Q♠', '3♣', '4♣', 'A♣', '8♣', '2♣', 'K♠',
    'K♣', 'A♦', '2♦', '3♦', '4♦', '6♣'
]

solitaire = solitaire(deckConfig)
cipherText =("SCYWLWXCACDWWIFZSXIMHVMBRIWHCLNLMZIHHWWCHVOZNJCKPPALVNMGFNJRLCQFHDKNHZHKRAGIFXGKQQSLNEDGKOTOFRFNZAJOWWVZAPGGMLURKZGQDMHEHKYEBLRUPMRPKFHFFMCIDKGYLOFLQQLSOMYAEGCPDYRWWJLTXRKQLOLXGCHCSCQMDUKZWMLMKNTHMJQNVORTTIDRHQZBEIJCJNTMRTHYNVGAID")

print(solitaire.decipher(cipherText, solitaire.keyedDeck))
print(f'Solitaire key deck: {solitaire.keyedDeck}')

# Decrypt: ANDTHENABRUPTLYANDUNBIDDENTHERECAMEINTOMYMINDASTORYOFTHEOLDWESTTHESTORYOFHOWINTHEPIONEERDAYSAGAMBLERSITTINGDOWNTOPLAYSOLITAIRELAIDHISGUNONTHETABLEBESIDEHIMANDIFHECAUGHTHIMSELFCHEATINGADMINISTEREDJUSTICEFIRSTHANDBYSHOOTINGHIMSELFXX
