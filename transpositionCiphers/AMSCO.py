# to be used in hillClimb.py with withoutClimbingLimit = 100

from numpy import argsort
import random

from permutationKey import permutationKey

class AMSCO():

    def __init__(self,cipher):
        self.__cipher = cipher
        self.__length = len(cipher)
        self.__key = permutationKey(range(2,int(self.__length**0.5)))
        self.__firstRowBoxBigram = True
        self.updateKeyLength()

    def shuffle(self):
        self.__key.shuffle()

    def undoShuffle(self):
        self.__key.undoShuffle()

    def shake(self):
        if random.random() > 0.5:
            self.__key.shake()
        else:
            self.__firstRowBoxBigram = not self.__firstRowBoxBigram

        self.updateKeyLength()

    def updateKeyLength(self):
        self.__keyLength = self.__key.getLength()

        if self.__keyLength%2 == 0:
            rowLength = 3 * (self.__keyLength // 2)

            self.__numberOfFilledRows,self.__leftOver = divmod(self.__length, rowLength)

        else:
            longRowLength = 3 * (self.__keyLength // 2) + 2
            shortRowLength = longRowLength - 1

            if self.__firstRowBoxBigram:

                if self.__length%(longRowLength+shortRowLength) < longRowLength:
                    self.__numberOfFilledRows = 2*(self.__length//(longRowLength+shortRowLength))
                    self.__leftOver = self.__length-self.__numberOfFilledRows*(longRowLength+shortRowLength)/2
                else:
                    IveGivenUpThinkingOfVariableNames = 2 * (self.__length // (longRowLength + shortRowLength))
                    self.__leftOver = self.__length - IveGivenUpThinkingOfVariableNames*(longRowLength+shortRowLength)/2 - longRowLength
                    self.__numberOfFilledRows = IveGivenUpThinkingOfVariableNames + 1

            else:

                if self.__length%(longRowLength+shortRowLength) < shortRowLength:
                    self.__numberOfFilledRows = 2*(self.__length//(longRowLength+shortRowLength))
                    self.__leftOver = self.__length-self.__numberOfFilledRows*(longRowLength+shortRowLength)/2
                else:
                    IveGivenUpThinkingOfVariableNames = 2 * (self.__length // (longRowLength + shortRowLength))
                    self.__leftOver = self.__length - IveGivenUpThinkingOfVariableNames*(longRowLength+shortRowLength)/2 - shortRowLength
                    self.__numberOfFilledRows = IveGivenUpThinkingOfVariableNames + 1

        lastRowBoxBigram = (self.__numberOfFilledRows % 2 == 0) ^ (not self.__firstRowBoxBigram)

        if self.__numberOfFilledRows % 2 == 0:
            longColumnLength = shortColumnLength = 3 * (self.__numberOfFilledRows // 2)
        else:
            longColumnLength = 3 * (self.__numberOfFilledRows // 2) + 2
            shortColumnLength = longColumnLength - 1

        self.__columnLengths = []

        # I understand this isn't the most efficient way to do this but the code is complicated enough as it is

        leftOver = self.__leftOver

        firstInColumnIsBigram = self.__firstRowBoxBigram

        for i in range(self.__keyLength):

            if firstInColumnIsBigram:
                columnLength = longColumnLength
                firstInColumnIsBigram = False
            else:
                columnLength = shortColumnLength
                firstInColumnIsBigram = True

            if leftOver > 0:

                if lastRowBoxBigram:
                    if leftOver == 1:
                        self.__columnLengths.append(columnLength + 1)
                    else:
                        self.__columnLengths.append(columnLength + 2)
                    leftOver -= 2
                    lastRowBoxBigram = False
                else:
                    self.__columnLengths.append(columnLength + 1)
                    leftOver -= 1
                    lastRowBoxBigram = True

            else:
                self.__columnLengths.append(columnLength)

    def decipher(self):

        plainText = []

        key = self.__key.getKey()

        place = 0

        distanceAlongColumns = []

        for column in argsort(key):

            distanceAlongColumns.append(place)

            place += self.__columnLengths[column]

        firstInColumnIsBigram = self.__firstRowBoxBigram

        for row in range(self.__numberOfFilledRows):

            currentColumnIsBigram = firstInColumnIsBigram
            for column in key:

                if currentColumnIsBigram:

                    plainText.append(self.__cipher[distanceAlongColumns[column]])
                    plainText.append(self.__cipher[distanceAlongColumns[column] + 1])

                    distanceAlongColumns[column] += 2
                else:
                    plainText.append(self.__cipher[distanceAlongColumns[column]])

                    distanceAlongColumns[column] += 1

                currentColumnIsBigram = not currentColumnIsBigram

            firstInColumnIsBigram = not firstInColumnIsBigram

        leftOver = self.__leftOver

        currentColumnIsBigram = firstInColumnIsBigram
        for column in key:

            if leftOver == 0:
                break

            if currentColumnIsBigram:

                plainText.append(self.__cipher[distanceAlongColumns[column]])

                if leftOver != 1:
                    plainText.append(self.__cipher[distanceAlongColumns[column] + 1])
                else:
                    break

                distanceAlongColumns[column] += 2
                leftOver -= 2
            else:
                plainText.append(self.__cipher[distanceAlongColumns[column]])

                distanceAlongColumns[column] += 1
                leftOver -= 1

            currentColumnIsBigram = not currentColumnIsBigram

        return plainText
