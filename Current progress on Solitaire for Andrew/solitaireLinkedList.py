import random

class listNode:
    def __init__(self,value):
        self.value = value
        self.next = None
        self.previous = None

class solitaireLinkedList:
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

        self.__initialDeck = self.__knownDeck.copy()

        cardsMissing = list(cardsMissing)

        place = 0
        for i,card in enumerate(self.__knownDeck):
            if card == "?":
                self.__initialDeck[i] = cardsMissing[place]

                place += 1

    def setCipher(self,cipher):
        self.__cipher = cipher

    # TEMPORARY:
    def setDeck(self,deckArray):
        self.__initialDeck = deckArray

        for i,card in enumerate(self.__initialDeck):
            if card == 53:
                self.__initialJokerA = i
            elif card == 54:
                self.__initialJokerB = i

    def shuffle(self):

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
            return 53
        if card == 'joker B':
            self.__initialJokerB = index
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

    def insertCardAfterCard(self,cardInserting,cardBefore):
        cardAfter = cardBefore.next
        cardBefore.next = cardInserting
        cardInserting.previous = cardBefore
        cardInserting.next = cardAfter
        cardAfter.previous = cardInserting

    def disconnectCard(self,card):
        card.previous.next = card.next
        card.next.previous = card.previous

    def moveCard(self,cardMoving,cardBeforeDestination):
        self.disconnectCard(cardMoving)
        self.insertCardAfterCard(cardMoving,cardBeforeDestination)

    def connectCards(self,cardBefore,cardAfter):
        cardBefore.next = cardAfter
        cardAfter.previous = cardBefore

    def getDeckArrayBackwards(self):
        array = []

        currentCard = self.__bottomCard

        # temporarty:
        iterations = 0

        while currentCard != self.__topCard and iterations < 100:
            iterations += 1
            array.append(currentCard.value)
            currentCard = currentCard.previous
        array.append(currentCard.value)

        """
        for _ in range(100):
            if currentCard == None:
                break
            array.append(currentCard.value)
            currentCard = currentCard.next
        """

        return array[::-1]

    def getDeckArray(self):
        array = []

        currentCard = self.__topCard

        # temporarty:
        iterations = 0

        while currentCard != self.__bottomCard and iterations < 100:
            iterations += 1
            array.append(currentCard.value)
            currentCard = currentCard.next
        array.append(currentCard.value)

        """
        for _ in range(100):
            if currentCard == None:
                break
            array.append(currentCard.value)
            currentCard = currentCard.next
        """

        return array

    def moveJokerA(self):

        # If jokerA on bottom, put it just after the top card, else swap joker A with card below it
        if self.__jokerAPosition == 53:
            self.__bottomCard = self.__jokerA.previous

            self.insertCardAfterCard(self.__jokerA,self.__topCard)

            self.__jokerAPosition = 1
            if self.__jokerBPosition != 0:
                self.__jokerBPosition += 1

        else:
            if self.__jokerAPosition == 52:
                self.disconnectCard(self.__jokerA)
                self.connectCards(self.__bottomCard,self.__jokerA)
                self.__bottomCard = self.__jokerA

            elif self.__jokerAPosition == 0:
                self.__topCard = self.__jokerA.next
                self.insertCardAfterCard(self.__jokerA,self.__topCard)

            else:
                self.moveCard(self.__jokerA,self.__jokerA.next)

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

            self.__bottomCard = self.__jokerB.previous
            self.insertCardAfterCard(self.__jokerB,self.__topCard.next)

            self.__jokerBPosition = 2
            if self.__jokerAPosition >= 2:
                self.__jokerAPosition += 1

        elif self.__jokerBPosition == 52:

            self.moveCard(self.__jokerB,self.__topCard)

            self.__jokerBPosition = 1
            if self.__jokerAPosition != 0:
                self.__jokerAPosition += 1
        else:
            if self.__jokerBPosition == 51:

                self.disconnectCard(self.__jokerB)
                self.connectCards(self.__bottomCard,self.__jokerB)
                self.__bottomCard = self.__jokerB

            elif self.__jokerBPosition == 0:

                self.__topCard = self.__jokerB.next
                self.insertCardAfterCard(self.__jokerB,self.__jokerB.next.next)
            else:

                self.moveCard(self.__jokerB,self.__jokerB.next.next)

            self.__jokerBPosition += 2
            if self.__jokerBPosition - 2 < self.__jokerAPosition <= self.__jokerBPosition:
                self.__jokerAPosition -= 1

    # triple cut - swap stack of cards above 1st joker with stack of cards below 2nd joker
    # 1st joker = joker close to the top
    def tripleCut(self):

        # print(self.getDeckArray())
        # print(self.__topCard.value)
        # print(self.__jokerA.value)

        if self.__jokerAPosition == 0:

            newTop = self.__jokerB.next
            newBottom = self.__jokerB
            # print(newBottom.value)

            self.connectCards(self.__bottomCard, self.__jokerA)

            self.__topCard = newTop
            self.__bottomCard = newBottom
            # print(self.__bottomCard.value)

        elif self.__jokerBPosition == 0:
            newTop = self.__jokerA.next
            newBottom = self.__jokerA

            self.connectCards(self.__bottomCard, self.__jokerB)

            self.__topCard = newTop
            self.__bottomCard = newBottom

        elif self.__jokerAPosition < self.__jokerBPosition:
            if self.__jokerBPosition == 53:
                newTop = self.__jokerA
                newBottom = self.__jokerA.previous
            else:
                newTop = self.__jokerB.next
                newBottom = self.__jokerA.previous

                self.connectCards(self.__bottomCard, self.__jokerA)

            # print(newBottom.value)

            self.connectCards(self.__jokerB, self.__topCard)

            self.__topCard = newTop
            self.__bottomCard = newBottom
            # print(self.__bottomCard.value)

        elif self.__jokerBPosition < self.__jokerAPosition:
            if self.__jokerAPosition == 53:
                newTop = self.__jokerB
                newBottom = self.__jokerB.previous
            else:
                newTop = self.__jokerA.next
                newBottom = self.__jokerB.previous

                self.connectCards(self.__bottomCard, self.__jokerB)

            # print(newBottom.value)

            self.connectCards(self.__jokerA, self.__topCard)

            self.__topCard = newTop
            self.__bottomCard = newBottom
            # print(self.__bottomCard.value)

        self.__jokerAPosition, self.__jokerBPosition = 53 - self.__jokerBPosition, 53 - self.__jokerAPosition

    # count cut -  Look at the bottom card. If it is a joker, do nothing for this step.
    # Else - take the number corresponding to that card and do a count cut by taking a stack of that many card off the top of the deck and putting that stack just above the bottom card.

    def countCut(self):

        if self.__jokerAPosition == 53 or self.__jokerBPosition == 53:
            return

        if self.__bottomCard.value <= 26:
            currentCard = self.__topCard
            for _ in range(self.__bottomCard.value-1):
                currentCard = currentCard.next

        else:
            currentCard = self.__bottomCard
            for _ in range(54-self.__bottomCard.value):
                currentCard = currentCard.previous

        newTopCard = currentCard.next

        self.connectCards(self.__bottomCard.previous, self.__topCard)
        self.connectCards(currentCard,self.__bottomCard)

        self.__topCard = newTopCard

        if self.__jokerAPosition < self.__bottomCard.value:
            self.__jokerAPosition += 53 - self.__bottomCard.value
        else:
            self.__jokerAPosition -= self.__bottomCard.value

        if self.__jokerBPosition < self.__bottomCard.value:
            self.__jokerBPosition += 53 - self.__bottomCard.value
        else:
            self.__jokerBPosition -= self.__bottomCard.value

    # generate keystream
    def generateKeystreamVal(self):
        while True:

            """
            if len(self.getDeckArray()) != 54 or set(self.getDeckArray()) != set(range(1,55)) or len(self.getDeckArrayBackwards()) != 54 or set(self.getDeckArrayBackwards()) != set(range(1,55)) or self.getDeckArray() != self.getDeckArrayBackwards() or self.getDeckArray()[self.__jokerAPosition] != 53 or  self.getDeckArray()[self.__jokerBPosition] != 54:
                print("before move:",self.getDeckArray())
                print("backwards: ",self.getDeckArrayBackwards())
                exit(1)
            """

            self.moveJokerA()

            """
            if len(self.getDeckArray()) != 54 or set(self.getDeckArray()) != set(range(1,55)) or len(self.getDeckArrayBackwards()) != 54 or set(self.getDeckArrayBackwards()) != set(range(1,55)) or self.getDeckArray() != self.getDeckArrayBackwards() or self.getDeckArray()[self.__jokerAPosition] != 53 or  self.getDeckArray()[self.__jokerBPosition] != 54:
                print("move A:", self.getDeckArray())
                print("backwards: ", self.getDeckArrayBackwards())
                exit(1)
            """

            self.moveJokerB()

            """
            if len(self.getDeckArray()) != 54 or set(self.getDeckArray()) != set(range(1,55)) or len(self.getDeckArrayBackwards()) != 54 or set(self.getDeckArrayBackwards()) != set(range(1,55)) or self.getDeckArray() != self.getDeckArrayBackwards() or self.getDeckArray()[self.__jokerAPosition] != 53 or  self.getDeckArray()[self.__jokerBPosition] != 54:
                print("move B:", self.getDeckArray())
                print("backwards: ", self.getDeckArrayBackwards())
                exit(1)
            """

            self.tripleCut()

            """
            if len(self.getDeckArray()) != 54 or set(self.getDeckArray()) != set(range(1,55)) or len(self.getDeckArrayBackwards()) != 54 or set(self.getDeckArrayBackwards()) != set(range(1,55)) or self.getDeckArray() != self.getDeckArrayBackwards() or self.getDeckArray()[self.__jokerAPosition] != 53 or  self.getDeckArray()[self.__jokerBPosition] != 54:
                print("triple cut:", self.getDeckArray())
                print("backwards: ", self.getDeckArrayBackwards())
                exit(1)
            """

            self.countCut()

            """
            if len(self.getDeckArray()) != 54 or set(self.getDeckArray()) != set(range(1,55)) or len(self.getDeckArrayBackwards()) != 54 or set(self.getDeckArrayBackwards()) != set(range(1,55)) or self.getDeckArray() != self.getDeckArrayBackwards() or self.getDeckArray()[self.__jokerAPosition] != 53 or  self.getDeckArray()[self.__jokerBPosition] != 54:
                print("count cut:", self.getDeckArray())
                print("backwards: ", self.getDeckArrayBackwards())
                exit(1)
            """

            topVal = self.__topCard.value

            if topVal == 54:
                topVal = 53

            currentCard = self.__topCard
            # could potentially do a check here and count down from the last pointer if list values have two way connectivity
            for _ in range(topVal):
                currentCard = currentCard.next

            newTopVal = currentCard.value

            # if newTopVal = 53, repeat from step 1
            if newTopVal == 53 or newTopVal == 54:
                continue

            return newTopVal

    def decipher(self):

        # for further optimisation, loop up until a joker without checking, then add the joker, and so on
        # keep track of where jokers are by algorithm in the array version
        # though gains will likely be small, I don't think they'll be negligible

        self.__topCard = listNode(self.__initialDeck[0])

        if self.__topCard.value == 53:
            self.__jokerA = self.__topCard
        elif self.__topCard.value == 54:
            self.__jokerB = self.__topCard

        previousCard = self.__topCard
        for i in range(1,53):
            currentCard = listNode(self.__initialDeck[i])

            if currentCard.value == 53:
                self.__jokerA = currentCard
            elif currentCard.value == 54:
                self.__jokerB = currentCard

            self.connectCards(previousCard,currentCard)

            previousCard = currentCard

        self.__bottomCard = listNode(self.__initialDeck[53])
        self.connectCards(previousCard,self.__bottomCard)

        if self.__bottomCard.value == 53:
            self.__jokerA = self.__bottomCard
        elif self.__bottomCard.value == 54:
            self.__jokerB = self.__bottomCard

        self.__jokerAPosition = self.__initialJokerA
        self.__jokerBPosition = self.__initialJokerB

        plainText = []
        for letter in self.__cipher:
            keyVal = self.generateKeystreamVal()

            plainVal = (letter - keyVal)

            plainText.append(plainVal%26)

        return plainText

    def getAdjacencyBonus(self):
        adjacencyBonus = 0
        previous = self.__initialDeck[0]
        for card in self.__initialDeck[1:]:
            adjacencyBonus += (card-previous)**2

        return -adjacencyBonus