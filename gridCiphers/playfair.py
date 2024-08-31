# To be run in hillClimbWithMargin. 
# Optimal conditions: 
# margin = 0.2*length
# chance to shuffle = 5*math.e**(0.1*score/length))
# add the adjacency bonus to the evaluated score in a 1:1 ratio i.e:
# def evaluate(plainText)
#     return cipher.getAdjacencyBonus() + evaluateQuadgramFrequencies(plainText)
# and run the hill climb with the above evaluate

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

    def getAdjacencyBonus(self):
        return self.__key.getAdjacencyBonus()
