# To be run in hillClimb. Optimal conditions: shake threshold: 100 shake amount: 1

from polybiusGridEnhancedShuffle import polybiusGridEnhancedShuffle

class playfair:
    def __init__(self, cipherText):
        self.__cipherText = cipherText
        self.__key = polybiusGridEnhancedShuffle()

    def decipher(self):

        plainText = []
        for i in range(0, len(self.__cipherText), 2):
            a = self.__cipherText[i]
            b = self.__cipherText[i + 1]
            plainText.extend(self.decodePair(a, b))
        # print(plainText)
        return plainText

    def decodePair(self, a, b):

        posA = self.__key.getCoordinatesOfCharacter(a)
        posB = self.__key.getCoordinatesOfCharacter(b)

        colA, rowA = posA
        colB, rowB = posB

        if rowA == rowB:
            # same row= shift columns left
            newA = self.__key.getCharacterAtCoordinates((colA - 1) % 5,rowA)
            newB = self.__key.getCharacterAtCoordinates((colB - 1) % 5,rowB)
        elif colA == colB:
            # same col= shift rows up
            newA = self.__key.getCharacterAtCoordinates(colA,(rowA - 1) % 5)
            newB = self.__key.getCharacterAtCoordinates(colB,(rowB - 1) % 5)
        else:
            # swap columns but keep rows
            newA = self.__key.getCharacterAtCoordinates(colB,rowA)
            newB = self.__key.getCharacterAtCoordinates(colA,rowB)

        return [newA, newB]

    def shuffle(self):
        self.__key.shuffle()

    def undoShuffle(self):
        self.__key.undoShuffle()
