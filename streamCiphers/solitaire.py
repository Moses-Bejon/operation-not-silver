import random

class solitaire:
    def __init__(self,cipher,initialDeck):
        self.__suits = {
            '♣': 0,
            '♦': 13,
            '♥': 26,
            '♠': 39
        }

        self.__cipher = cipher

        cardsMissing = set(range(1, 53))
        cardsMissing.add("A")
        cardsMissing.add("B")

        self.__unknownIndices = []
        self.__knownDeck = []
        for i,card in enumerate(initialDeck):
            card = self.cardToVal(card,i)
            self.__knownDeck.append(card)

            if card == "?":
                self.__unknownIndices.append(i)
            else:
                cardsMissing.discard(card)

        self.__initialDeck = self.__knownDeck.copy()

        cardsMissing = list(cardsMissing)

        place = 0
        for i,card in enumerate(self.__knownDeck):
            if card == "?":
                self.__initialDeck[i] = cardsMissing[place]

                if cardsMissing[place] == "A":
                    self.__initialJokerA = i
                elif cardsMissing[place] == "B":
                    self.__initialJokerB = i

                place += 1

    def setCipher(self,cipher):
        self.__cipher = cipher

    def shuffle(self):

        """
        # TEST
        if self.__initialJokerA != self.__initialDeck.index("A"):
            print("TEST FAILED, joker A")
            exit(1)
        if self.__initialJokerB != self.__initialDeck.index("B"):
            print("TEST FAILED, joker B")
            exit(1)
        """

        if random.random() > 0.5:
            self.__cards = random.sample(self.__unknownIndices,k=2)
            self.__initialDeck[self.__cards[0]],self.__initialDeck[self.__cards[1]] = self.__initialDeck[self.__cards[1]],self.__initialDeck[self.__cards[0]]

            if self.__cards[0] == self.__initialJokerA:
                self.__initialJokerA = self.__cards[1]
            elif self.__cards[1] == self.__initialJokerA:
                self.__initialJokerA = self.__cards[0]

            if self.__cards[0] == self.__initialJokerB:
                self.__initialJokerB = self.__cards[1]
            elif self.__cards[1] == self.__initialJokerB:
                self.__initialJokerB = self.__cards[0]

        else:
            self.__cards = random.sample(self.__unknownIndices, k=3)
            self.__initialDeck[self.__cards[0]], self.__initialDeck[self.__cards[1]] = self.__initialDeck[self.__cards[1]], self.__initialDeck[self.__cards[0]]
            self.__initialDeck[self.__cards[0]], self.__initialDeck[self.__cards[2]] = self.__initialDeck[self.__cards[2]], self.__initialDeck[self.__cards[0]]

            if self.__cards[0] == self.__initialJokerA:
                self.__initialJokerA = self.__cards[1]
            elif self.__cards[1] == self.__initialJokerA:
                self.__initialJokerA = self.__cards[2]
            elif self.__cards[2] == self.__initialJokerA:
                self.__initialJokerA = self.__cards[0]

            if self.__cards[0] == self.__initialJokerB:
                self.__initialJokerB = self.__cards[1]
            elif self.__cards[1] == self.__initialJokerB:
                self.__initialJokerB = self.__cards[2]
            elif self.__cards[2] == self.__initialJokerB:
                self.__initialJokerB = self.__cards[0]

    def undoShuffle(self):

        """
        # TEST
        if self.__initialJokerA != self.__initialDeck.index("A"):
            print("TEST FAILED, joker A")
            exit(1)
        if self.__initialJokerB != self.__initialDeck.index("B"):
            print("TEST FAILED, joker B")
            exit(1)
        """

        if len(self.__cards) == 2:
            self.__initialDeck[self.__cards[0]],self.__initialDeck[self.__cards[1]] = self.__initialDeck[self.__cards[1]],self.__initialDeck[self.__cards[0]]

            if self.__cards[0] == self.__initialJokerA:
                self.__initialJokerA = self.__cards[1]
            elif self.__cards[1] == self.__initialJokerA:
                self.__initialJokerA = self.__cards[0]

            if self.__cards[0] == self.__initialJokerB:
                self.__initialJokerB = self.__cards[1]
            elif self.__cards[1] == self.__initialJokerB:
                self.__initialJokerB = self.__cards[0]
        else:
            self.__initialDeck[self.__cards[0]], self.__initialDeck[self.__cards[2]] = self.__initialDeck[self.__cards[2]], self.__initialDeck[self.__cards[0]]
            self.__initialDeck[self.__cards[0]], self.__initialDeck[self.__cards[1]] = self.__initialDeck[self.__cards[1]], self.__initialDeck[self.__cards[0]]

            if self.__cards[1] == self.__initialJokerA:
                self.__initialJokerA = self.__cards[0]
            elif self.__cards[2] == self.__initialJokerA:
                self.__initialJokerA = self.__cards[1]
            elif self.__cards[0] == self.__initialJokerA:
                self.__initialJokerA = self.__cards[2]

            if self.__cards[1] == self.__initialJokerB:
                self.__initialJokerB = self.__cards[0]
            elif self.__cards[2] == self.__initialJokerB:
                self.__initialJokerB = self.__cards[1]
            elif self.__cards[0] == self.__initialJokerB:
                self.__initialJokerB = self.__cards[2]

    # convert deck of cards to numbers
    def cardToVal(self, card,index):
        if card == 'joker A':
            self.__initialJokerA = index
            return "A"
        if card == 'joker B':
            self.__initialJokerB = index
            return "B"
        if card == '?':
            return "?"

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

        val = self.__suits[suit]
        return val + rank

    def moveJokerA(self):
        # If jokerA on bottom, put it just after the top card, else swap joker A with card below it
        if self.__jokerA == 53:
            self.__deck.insert(1, self.__deck.pop())
            self.__jokerA = 1

            if self.__jokerB != 0:
                self.__jokerB += 1

        else:
            self.__deck[self.__jokerA], self.__deck[self.__jokerA+1] = self.__deck[self.__jokerA+1], self.__deck[self.__jokerA]
            self.__jokerA += 1

            if self.__jokerA == self.__jokerB:
                self.__jokerB -= 1

    def moveJokerB(self):
        # If joker B is on the bottom of the deck, put it just after the second card.
        # If joker B is the second to-last card, put it just after the top card.
        # If neither of these is the case, move joker B down by two cards.
        if self.__jokerB == 53:
            self.__deck.insert(2, self.__deck.pop())
            self.__jokerB = 2

            if self.__jokerA >= 2:
                self.__jokerA += 1

        elif self.__deck[-2] == "B":
            self.__deck.insert(1, self.__deck.pop(-2))
            self.__jokerB = 1

            if self.__jokerA != 0:
                self.__jokerA += 1

        else:
            self.__deck[self.__jokerB], self.__deck[self.__jokerB + 1] = self.__deck[self.__jokerB + 1], self.__deck[self.__jokerB]
            self.__jokerB += 1
            if self.__jokerA == self.__jokerB:
                self.__jokerA -= 1

            self.__deck[self.__jokerB], self.__deck[self.__jokerB + 1] = self.__deck[self.__jokerB + 1], self.__deck[self.__jokerB]
            self.__jokerB += 1
            if self.__jokerA == self.__jokerB:
                self.__jokerA -= 1

    # triple cut - swap stack of cards above 1st joker with stack of cards below 2nd joker
    # 1st joker = joker close to the top
    def tripleCut(self):
        if self.__jokerA > self.__jokerB:
            self.__deck = self.__deck[self.__jokerA + 1:] + self.__deck[self.__jokerB:self.__jokerA + 1] + self.__deck[:self.__jokerB]
        else:
            self.__deck = self.__deck[self.__jokerB + 1:] + self.__deck[self.__jokerA:self.__jokerB + 1] + self.__deck[:self.__jokerA]

        self.__jokerA,self.__jokerB = 53 - self.__jokerB,53 - self.__jokerA


    # count cut -  Look at the bottom card. If it is a joker, do nothing for this step.
    # Else - take the number corresponding to that card and do a count cut by taking a stack of that many card off the top of the deck and putting that stack just above the bottom card.

    def countCut(self):
        if self.__jokerA == 53 or self.__jokerB == 53:
            return

        bottomVal = self.__deck[-1]
        self.__deck = self.__deck[bottomVal:-1] + self.__deck[:bottomVal] + [self.__deck[-1]]

        if self.__jokerA < bottomVal:
            self.__jokerA += 53 - bottomVal
        else:
            self.__jokerA -= bottomVal

        if self.__jokerB < bottomVal:
            self.__jokerB += 53 - bottomVal
        else:
            self.__jokerB -= bottomVal

    def cardVal(self, card):
        if card == "A" or card == "B":
            return 53
        return card

    # generate keystream
    def generateKeystreamVal(self):
        while True:

            """
            # TEST
            if self.__jokerA != self.__deck.index("A"):
                print("TEST FAILED BEFORE MOVE, joker A")
                exit(1)
            if self.__jokerB != self.__deck.index("B"):
                print("TEST FAILED BEFORE MOVE, joker B")
                exit(1)
            """

            self.moveJokerA()

            """
            # TEST
            if self.__jokerA != self.__deck.index("A"):
                print("TEST FAILED AFTER A MOVE, joker A")
                exit(1)
            if self.__jokerB != self.__deck.index("B"):
                print("TEST FAILED AFTER A MOVE, joker B")
                exit(1)
            """

            self.moveJokerB()

            """
            # TEST
            if self.__jokerA != self.__deck.index("A"):
                print("TEST FAILED AFTER B MOVE, joker A")
                exit(1)
            if self.__jokerB != self.__deck.index("B"):
                print("TEST FAILED AFTER B MOVE, joker B")
                exit(1)
            """

            self.tripleCut()

            """
            # TEST
            if self.__jokerA != self.__deck.index("A"):
                print("TEST FAILED AFTER TRIPLE CUT, joker A")
                exit(1)
            if self.__jokerB != self.__deck.index("B"):
                print("TEST FAILED AFTER TRIPLE CUT, joker B")
                exit(1)
            """

            self.countCut()

            """
            # TEST
            if self.__jokerA != self.__deck.index("A"):
                print("TEST FAILED AFTER COUNT CUT, joker A")
                exit(1)
            if self.__jokerB != self.__deck.index("B"):
                print("TEST FAILED AFTER COUNT CUT, joker B")
                exit(1)
            """

            topVal = self.__deck[0]

            if topVal == "A" or topVal == "B":
                topVal = 53

            # New top card after stack
            newTopVal = self.__deck[topVal]

            # if newTopVal = 53, repeat from step 1
            if newTopVal == "A" or newTopVal == "B":
                continue

            return newTopVal

    def decipher(self):
        self.__deck = self.__initialDeck.copy()
        self.__jokerA = self.__initialJokerA
        self.__jokerB = self.__initialJokerB

        plainText = []
        for letter in self.__cipher:
            keyVal = self.generateKeystreamVal()

            plainVal = (letter - keyVal)
            if plainVal == 0:
                plainVal = 26

            plainText.append(plainVal%26)

        return plainText
