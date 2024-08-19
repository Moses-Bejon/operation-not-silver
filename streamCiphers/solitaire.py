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

    def moveJokerA(self):
        # If jokerA on bottom, put it just after the top card, else swap joker A with card below it
        if self.__deck[-1] == self.jokerA:
            self.__deck.insert(1, self.__deck.pop())
        else:
            index = self.__deck.index(self.jokerA)
            self.__deck[index], self.__deck[index+1] = self.__deck[index+1], self.__deck[index]

    def moveJokerB(self):
        # If joker B is on the bottom of the deck, put it just after the second card.
        # If joker B is the second to-last card, put it just after the top card.
        # If neither of these is the case, move joker B down by two cards.
        if self.__deck[-1] == self.jokerB:
            if len(self.__deck) > 2:
                self.__deck.insert(2, self.__deck.pop())
            else:
                self.__deck.insert(1, self.__deck.pop())
        elif self.__deck[-2] == self.jokerB:
            self.__deck.insert(1, self.__deck.pop(-2))
        else:
            index = self.__deck.index(self.jokerB)
            self.__deck.insert((index + 2) % len(self.__deck), self.__deck.pop(index))

    # triple cut - swap stack of cards above 1st joker with stack of cards below 2nd joker
    # 1st joker = joker close to the top
    def tripleCut(self):
        firstJoker = min(self.__deck.index(self.jokerA), self.__deck.index(self.jokerB))
        secondJoker = max(self.__deck.index(self.jokerA), self.__deck.index(self.jokerB))
        self.__deck = self.__deck[secondJoker + 1:] + self.__deck[firstJoker:secondJoker + 1] + self.__deck[:firstJoker]

    # count cut -  Look at the bottom card. If it is a joker, do nothing for this step.
    # Else - take the number corresponding to that card and do a count cut by taking a stack of that many card off the top of the deck and putting that stack just above the bottom card.

    def countCut(self):
        bottomVal = self.cardVal(self.__deck[-1])
        if bottomVal in [self.jokerA, self.jokerB]:
            return
        self.__deck = self.__deck[bottomVal:-1] + self.__deck[:bottomVal] + [self.__deck[-1]]

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
    def generateKeystreamVal(self):
        while True:
            self.moveJokerA()
            self.moveJokerB()
            self.tripleCut()
            self.countCut()

            topVal = self.__deck[0]

            if topVal == 54:
                topVal = 53

            # New top card after stack
            newTopVal = self.__deck[topVal]

            # if newTopVal = 53, repeat from step 1
            if newTopVal == 53 or newTopVal == 54:
                continue
            elif newTopVal > 26:
                newTopVal -= 26

            return newTopVal

    # generate required length of keystream
    def generateKeystream(self, deck, length):
        self.__deck = deck.copy()
        keystream = []
        for _ in range(length):
            keystream.append(self.generateKeystreamVal())
        return keystream

    def decipher(self, cipherText, deck):
        keystream = self.generateKeystream(deck.copy(), len(cipherText))
        print(f'Keystream: {keystream}')

        plainText = []
        for i, letter in enumerate(cipherText):
            cipherVal = self.letterToNum(letter)
            keyVal = keystream[i]

            plainVal = (cipherVal - keyVal)
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
