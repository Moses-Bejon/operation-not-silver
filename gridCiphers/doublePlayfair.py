# currently testing with hillClimbWithMargin 

from polybiusGridEnhancedShuffle import polybiusGridEnhancedShuffle
import random

class doublePlayfair:
    def __init__(self, cipherText):
        self.__cipherText = cipherText
        self.__key1 = polybiusGridEnhancedShuffle()
        self.__key2 = polybiusGridEnhancedShuffle()

    def shuffle(self):
        if random.random() > 0.5:
            self.__shuffledKey1 = True
            self.__key1.shuffle()
        else:
            self.__shuffledKey1 = False
            self.__key2.shuffle()

    def undoShuffle(self):
        if self.__shuffledKey1:
            self.__key1.undoShuffle()
        else:
            self.__key2.undoShuffle()

    def decipher(self):

        plainText = []

        for i in range(0, len(self.__cipherText),2):
            a = self.__cipherText[i]
            b = self.__cipherText[i+1]

            posA = self.__key1.getCoordinatesOfCharacter(a)
            posB = self.__key2.getCoordinatesOfCharacter(b)

            colA, rowA = posA
            colB, rowB = posB

            if rowA == rowB:
                # same row= shift columns left
                newA = self.__key1.getCharacterAtCoordinates((colA - 1) % 5, rowA)
                newB = self.__key2.getCharacterAtCoordinates((colB - 1) % 5, rowB)
            elif colA == colB:
                # same col= shift rows up
                newA = self.__key1.getCharacterAtCoordinates(colA, (rowA - 1) % 5)
                newB = self.__key2.getCharacterAtCoordinates(colB, (rowB - 1) % 5)
            else:
                # swap columns but keep rows
                newA = self.__key1.getCharacterAtCoordinates(colB, rowA)
                newB = self.__key2.getCharacterAtCoordinates(colA, rowB)

            plainText.append(newA)
            plainText.append(newB)

        return plainText
