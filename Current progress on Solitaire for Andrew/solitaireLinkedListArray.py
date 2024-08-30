import random

class linkedList():
    def __init__(self,array):

        self.__length = len(array)
        self.__halfLength = self.__length/2

        self.values = array
        self.resetPointers()

    def resetPointers(self):
        self.previousPointers = list(range(-1, self.__length - 1))
        self.nextPointers = list(range(1, self.__length + 1))

        self.firstPointer = 0
        self.lastPointer = 53

    def insertCardAfterCard(self,cardInsertingPointer,cardBeforePointer):
        cardAfterPointer = self.nextPointers[cardBeforePointer]
        self.nextPointers[cardBeforePointer] = cardInsertingPointer
        self.previousPointers[cardInsertingPointer] = cardBeforePointer
        self.nextPointers[cardInsertingPointer] = cardAfterPointer
        self.previousPointers[cardAfterPointer] = cardInsertingPointer

    def disconnectCard(self, cardPointer):
        self.nextPointers[self.previousPointers[cardPointer]] = self.nextPointers[cardPointer]
        self.previousPointers[self.nextPointers[cardPointer]] = self.previousPointers[cardPointer]

    def moveCard(self, cardMovingPointer, cardBeforeDestinationPointer):
        self.disconnectCard(cardMovingPointer)
        self.insertCardAfterCard(cardMovingPointer, cardBeforeDestinationPointer)

    def connectCards(self, cardBeforePointer, cardAfterPointer):
        self.nextPointers[cardBeforePointer] = cardAfterPointer
        self.previousPointers[cardAfterPointer] = cardBeforePointer

    def getArrayBackwards(self):
        array = []

        currentCardPointer = self.lastPointer

        # temporarty:
        iterations = 0

        while currentCardPointer != self.firstPointer and iterations < 100:
            iterations += 1
            array.append(self.values[currentCardPointer])
            currentCardPointer = self.previousPointers[currentCardPointer]
        array.append(self.values[currentCardPointer])

        return array[::-1]

    def getArray(self):
        array = []

        currentCardPointer = self.firstPointer

        # temporarty:
        iterations = 0

        while currentCardPointer != self.lastPointer and iterations < 100:
            iterations += 1
            array.append(self.values[currentCardPointer])
            currentCardPointer = self.nextPointers[currentCardPointer]
        array.append(self.values[currentCardPointer])

        return array

    def getPointerOfIndex(self,index):

        if index <= self.__halfLength:
            currentCardPointer = self.firstPointer

            for _ in range(index):
                currentCardPointer = self.nextPointers[currentCardPointer]
        else:
            currentCardPointer = self.lastPointer
            for _ in range(self.__length - index - 1):
                currentCardPointer = self.previousPointers[currentCardPointer]

        return currentCardPointer


class solitaireLinkedListArray:
    def __init__(self,cipher,initialDeck):
        self.__suits = {
            '♣': 0,
            '♦': 13,
            '♥': 26,
            '♠': 39
        }

        self.__cipher = cipher

        cardsMissing = set(range(1, 55))

        self.__unknownIndices = []
        self.__knownDeck = []
        for i,card in enumerate(initialDeck):
            card = self.cardToVal(card,i)
            self.__knownDeck.append(card)

            if card == "?":
                self.__unknownIndices.append(i)
            else:
                cardsMissing.discard(card)

        self.__deck = self.__knownDeck.copy()

        cardsMissing = list(cardsMissing)

        place = 0
        for i,card in enumerate(self.__knownDeck):
            if card == "?":
                self.__deck[i] = cardsMissing[place]

                place += 1

        self.__deck = linkedList(self.__deck)

    def setCipher(self,cipher):
        self.__cipher = cipher

    # TEMPORARY:
    def setDeck(self,deckArray):
        self.__deck = linkedList(deckArray)

        for i,card in enumerate(self.__deck.values):
            if card == 53:
                self.__jokerAPointer = i
            elif card == 54:
                self.__jokerBPointer = i

    def shuffle(self):

        if random.random() > 0.5:
            self.__cards = random.sample(self.__unknownIndices,k=2)
            self.__deck.values[self.__cards[0]],self.__deck.values[self.__cards[1]] = self.__deck.values[self.__cards[1]],self.__deck.values[self.__cards[0]]

            if self.__cards[0] == self.__jokerAPointer:
                self.__jokerAPointer = self.__cards[1]
            elif self.__cards[1] == self.__jokerAPointer:
                self.__jokerAPointer = self.__cards[0]

            if self.__cards[0] == self.__jokerBPointer:
                self.__jokerBPointer = self.__cards[1]
            elif self.__cards[1] == self.__jokerBPointer:
                self.__jokerBPointer = self.__cards[0]

        else:
            self.__cards = random.sample(self.__unknownIndices, k=3)
            self.__deck.values[self.__cards[0]], self.__deck.values[self.__cards[1]] = self.__deck.values[self.__cards[1]], self.__deck.values[self.__cards[0]]
            self.__deck.values[self.__cards[0]], self.__deck.values[self.__cards[2]] = self.__deck.values[self.__cards[2]], self.__deck.values[self.__cards[0]]

            if self.__cards[0] == self.__jokerAPointer:
                self.__jokerAPointer = self.__cards[1]
            elif self.__cards[1] == self.__jokerAPointer:
                self.__jokerAPointer = self.__cards[2]
            elif self.__cards[2] == self.__jokerAPointer:
                self.__jokerAPointer = self.__cards[0]

            if self.__cards[0] == self.__jokerBPointer:
                self.__jokerBPointer = self.__cards[1]
            elif self.__cards[1] == self.__jokerBPointer:
                self.__jokerBPointer = self.__cards[2]
            elif self.__cards[2] == self.__jokerBPointer:
                self.__jokerBPointer = self.__cards[0]

    def undoShuffle(self):

        if len(self.__cards) == 2:
            self.__deck.values[self.__cards[0]],self.__deck.values[self.__cards[1]] = self.__deck.values[self.__cards[1]],self.__deck.values[self.__cards[0]]

        if self.__cards[0] == self.__jokerAPointer:
            self.__jokerAPointer = self.__cards[1]
        elif self.__cards[1] == self.__jokerAPointer:
            self.__jokerAPointer = self.__cards[0]

        if self.__cards[0] == self.__jokerBPointer:
            self.__jokerBPointer = self.__cards[1]
        elif self.__cards[1] == self.__jokerBPointer:
            self.__jokerBPointer = self.__cards[0]

        else:
            self.__deck.values[self.__cards[0]], self.__deck.values[self.__cards[2]] = self.__deck.values[self.__cards[2]], self.__deck.values[self.__cards[0]]
            self.__deck.values[self.__cards[0]], self.__deck.values[self.__cards[1]] = self.__deck.values[self.__cards[1]], self.__deck.values[self.__cards[0]]

            if self.__cards[1] == self.__jokerAPointer:
                self.__jokerAPointer = self.__cards[0]
            elif self.__cards[2] == self.__jokerAPointer:
                self.__jokerAPointer = self.__cards[1]
            elif self.__cards[0] == self.__jokerAPointer:
                self.__jokerAPointer = self.__cards[2]

            if self.__cards[1] == self.__jokerBPointer:
                self.__jokerBPointer = self.__cards[0]
            elif self.__cards[2] == self.__jokerBPointer:
                self.__jokerBPointer = self.__cards[1]
            elif self.__cards[0] == self.__jokerBPointer:
                self.__jokerBPointer = self.__cards[2]

    # convert deck of cards to numbers
    def cardToVal(self, card,index):
        if card == 'joker A':
            self.__jokerAPointer = index
            return 53
        if card == 'joker B':
            self.__jokerBPointer = index
            return 54
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
        if self.__jokerAPosition == 53:
            self.__deck.lastPointer = self.__deck.previousPointers[self.__jokerAPointer]

            self.__deck.insertCardAfterCard(self.__jokerAPointer, self.__deck.firstPointer)

            self.__jokerAPosition = 1
            if self.__jokerBPosition != 0:
                self.__jokerBPosition += 1
        else:

            if self.__jokerAPosition == 52:
                self.__deck.disconnectCard(self.__jokerAPointer)
                self.__deck.connectCards(self.__deck.lastPointer,self.__jokerAPointer)
                self.__deck.lastPointer = self.__jokerAPointer

            elif self.__jokerAPointer == self.__deck.firstPointer:
                self.__deck.firstPointer = self.__deck.nextPointers[self.__jokerAPointer]
                self.__deck.insertCardAfterCard(self.__jokerAPointer, self.__deck.firstPointer)

            else:
                self.__deck.moveCard(self.__jokerAPointer, self.__deck.nextPointers[self.__jokerAPointer])

            self.__jokerAPosition += 1
            if self.__jokerAPosition == self.__jokerBPosition:
                self.__jokerBPosition -= 1

    def moveJokerB(self):

        # print(self.getDeckArray())
        # print(self.getDeckArrayBackwards())

        # If joker B is on the bottom of the deck, put it just after the second card.
        # If joker B is the second to-last card, put it just after the top card.
        # If neither of these is the case, move joker B down by two cards.
        if self.__jokerBPosition == 53:

            self.__deck.lastPointer = self.__deck.previousPointers[self.__jokerBPointer]
            self.__deck.insertCardAfterCard(self.__jokerBPointer, self.__deck.nextPointers[self.__deck.firstPointer])

            self.__jokerBPosition = 2
            if self.__jokerAPosition >= 2:
                self.__jokerAPosition += 1

        elif self.__jokerBPosition == 52:

            self.__deck.moveCard(self.__jokerBPointer, self.__deck.firstPointer)

            self.__jokerBPosition = 1
            if self.__jokerAPosition != 0:
                self.__jokerAPosition += 1

        else:

            if self.__jokerBPosition == 51:

                self.__deck.disconnectCard(self.__jokerBPointer)
                self.__deck.connectCards(self.__deck.lastPointer, self.__jokerBPointer)
                self.__deck.lastPointer = self.__jokerBPointer

            elif self.__jokerBPosition == 0:

                self.__deck.firstPointer = self.__deck.nextPointers[self.__jokerBPointer]
                self.__deck.insertCardAfterCard(self.__jokerBPointer, self.__deck.nextPointers[self.__deck.nextPointers[self.__jokerBPointer]])
            else:

                self.__deck.moveCard(self.__jokerBPointer, self.__deck.nextPointers[self.__deck.nextPointers[self.__jokerBPointer]])

            self.__jokerBPosition += 2
            if self.__jokerBPosition - 2 < self.__jokerAPosition <= self.__jokerBPosition:
                self.__jokerAPosition -= 1

    # triple cut - swap stack of cards above 1st joker with stack of cards below 2nd joker
    # 1st joker = joker close to the top
    def tripleCut(self):

        if self.__jokerAPosition == 0:
            newTop = self.__deck.nextPointers[self.__jokerBPointer]
            newBottom = self.__jokerBPointer
            # print(newBottom.value)

            self.__deck.connectCards(self.__deck.lastPointer, self.__jokerAPointer)

            self.__deck.firstPointer = newTop
            self.__deck.lastPointer = newBottom

        elif self.__jokerBPosition == 0:
            newTop = self.__deck.nextPointers[self.__jokerAPointer]
            newBottom = self.__jokerAPointer

            self.__deck.connectCards(self.__deck.lastPointer, self.__jokerBPointer)

            self.__deck.firstPointer = newTop
            self.__deck.lastPointer = newBottom

        elif self.__jokerAPosition < self.__jokerBPosition:
            if self.__jokerBPosition == 53:
                newTop = self.__jokerAPointer
                newBottom = self.__deck.previousPointers[self.__jokerAPointer]
            else:
                newTop = self.__deck.nextPointers[self.__jokerBPointer]
                newBottom = self.__deck.previousPointers[self.__jokerAPointer]

                self.__deck.connectCards(self.__deck.lastPointer, self.__jokerAPointer)

            # print(newBottom.value)

            self.__deck.connectCards(self.__jokerBPointer, self.__deck.firstPointer)

            self.__deck.firstPointer = newTop
            self.__deck.lastPointer = newBottom

        elif self.__jokerBPosition < self.__jokerAPosition:

            if self.__jokerAPosition == 53:
                newTop = self.__jokerBPointer
                newBottom = self.__deck.previousPointers[self.__jokerBPointer]
            else:
                newTop = self.__deck.nextPointers[self.__jokerAPointer]
                newBottom = self.__deck.previousPointers[self.__jokerBPointer]

                self.__deck.connectCards(self.__deck.lastPointer, self.__jokerBPointer)

            # print(newBottom.value)

            self.__deck.connectCards(self.__jokerAPointer, self.__deck.firstPointer)

            self.__deck.firstPointer = newTop
            self.__deck.lastPointer = newBottom

        self.__jokerAPosition, self.__jokerBPosition = 53 - self.__jokerBPosition, 53 - self.__jokerAPosition

        # print(self.__deck.getArray())
        # print(self.__deck.firstPointer.value)
        # print(self.__jokerA.value)

    # count cut -  Look at the bottom card. If it is a joker, do nothing for this step.
    # Else - take the number corresponding to that card and do a count cut by taking a stack of that many card off the top of the deck and putting that stack just above the bottom card.

    def countCut(self):

        if self.__jokerAPosition == 53 or self.__jokerBPosition == 53:
            return

        newTopCard = self.__deck.getPointerOfIndex(self.__deck.values[self.__deck.lastPointer])

        self.__deck.connectCards(self.__deck.previousPointers[self.__deck.lastPointer], self.__deck.firstPointer)
        self.__deck.connectCards(self.__deck.previousPointers[newTopCard],self.__deck.lastPointer)

        self.__deck.firstPointer = newTopCard

        if self.__jokerAPosition < self.__deck.values[self.__deck.lastPointer]:
            self.__jokerAPosition += 53 - self.__deck.values[self.__deck.lastPointer]
        else:
            self.__jokerAPosition -= self.__deck.values[self.__deck.lastPointer]

        if self.__jokerBPosition < self.__deck.values[self.__deck.lastPointer]:
            self.__jokerBPosition += 53 - self.__deck.values[self.__deck.lastPointer]
        else:
            self.__jokerBPosition -= self.__deck.values[self.__deck.lastPointer]

    # generate keystream
    def generateKeystreamVal(self):
        while True:

            """
            if len(self.__deck.getArray()) != 54 or set(self.__deck.getArray()) != set(range(1,55)) or len(self.__deck.getArrayBackwards()) != 54 or set(self.__deck.getArrayBackwards()) != set(range(1,55)) or self.__deck.getArray() != self.__deck.getArrayBackwards():
                print("before move:",self.__deck.getArray())
                print("backwards: ",self.__deck.getArrayBackwards())
                exit(1)
            """

            self.moveJokerA()

            """
            if len(self.__deck.getArray()) != 54 or set(self.__deck.getArray()) != set(range(1,55)) or len(self.__deck.getArrayBackwards()) != 54 or set(self.__deck.getArrayBackwards()) != set(range(1,55)) or self.__deck.getArray() != self.__deck.getArrayBackwards():
                print("move A:", self.__deck.getArray())
                print("backwards: ", self.__deck.getArrayBackwards())
                exit(1)
            """

            self.moveJokerB()

            """
            if len(self.__deck.getArray()) != 54 or set(self.__deck.getArray()) != set(range(1,55)) or len(self.__deck.getArrayBackwards()) != 54 or set(self.__deck.getArrayBackwards()) != set(range(1,55)) or self.__deck.getArray() != self.__deck.getArrayBackwards():
                print("move B:", self.__deck.getArray())
                print("backwards: ", self.__deck.getArrayBackwards())
                exit(1)
            """

            self.tripleCut()

            """
            if len(self.__deck.getArray()) != 54 or set(self.__deck.getArray()) != set(range(1,55)) or len(self.__deck.getArrayBackwards()) != 54 or set(self.__deck.getArrayBackwards()) != set(range(1,55)) or self.__deck.getArray() != self.__deck.getArrayBackwards():
                print("triple cut:", self.__deck.getArray())
                print("backwards: ", self.__deck.getArrayBackwards())
                exit(1)
            """

            self.countCut()

            """
            if len(self.__deck.getArray()) != 54 or set(self.__deck.getArray()) != set(range(1,55)) or len(self.__deck.getArrayBackwards()) != 54 or set(self.__deck.getArrayBackwards()) != set(range(1,55)) or self.__deck.getArray() != self.__deck.getArrayBackwards():
                print("count cut:", self.__deck.getArray())
                print("backwards: ", self.__deck.getArrayBackwards())
                exit(1)
            """

            topVal = self.__deck.values[self.__deck.firstPointer]

            if topVal == 54:
                topVal = 53

            newTopVal = self.__deck.values[self.__deck.getPointerOfIndex(topVal)]

            # if newTopVal = 53, repeat from step 1
            if newTopVal == 53 or newTopVal == 54:
                continue

            return newTopVal

    def decipher(self):

        # for further optimisation, loop up until a joker without checking, then add the joker, and so on
        # keep track of where jokers are by algorithm in the array version
        # though gains will likely be small, I don't think they'll be negligible

        self.__deck.resetPointers()

        self.__jokerAPosition = self.__jokerAPointer
        self.__jokerBPosition = self.__jokerBPointer

        plainText = []
        for letter in self.__cipher:
            keyVal = self.generateKeystreamVal()

            plainVal = (letter - keyVal)

            plainText.append(plainVal%26)

        return plainText

    def getAdjacencyBonus(self):
        adjacencyBonus = 0
        previous = self.__deck.values[0]
        for card in self.__deck.values[1:]:
            adjacencyBonus += (card-previous)**2

        return -adjacencyBonus