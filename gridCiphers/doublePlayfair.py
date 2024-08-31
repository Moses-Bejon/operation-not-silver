from polybiusGridEnhancedShuffle import polybiusGridEnhancedShuffle
from verticalTwoSquare import verticalTwoSquare 

class doublePlayfair(verticalTwoSquare):
    def __init__(self, cipher):
        super().__init__(cipher)
        self._grid1 = polybiusGridEnhancedShuffle()
        self._grid2 = polybiusGridEnhancedShuffle()

    def decipher(self):

        plainText = []

        for i in range(0, len(self._cipher), 2):
            a = self._cipher[i]
            b = self._cipher[i + 1]

            posA = self._grid1.getCoordinatesOfCharacter(a)
            posB = self._grid2.getCoordinatesOfCharacter(b)

            colA, rowA = posA
            colB, rowB = posB

            if rowA == rowB:
                # same row= shift columns left
                newA = self._grid1.getCharacterAtCoordinates((colA - 1) % 5, rowA)
                newB = self._grid2.getCharacterAtCoordinates((colB - 1) % 5, rowB)
            elif colA == colB:
                # same col= shift rows up
                newA = self._grid1.getCharacterAtCoordinates(colA, (rowA - 1) % 5)
                newB = self._grid2.getCharacterAtCoordinates(colB, (rowB - 1) % 5)
            else:
                # swap columns but keep rows
                newA = self._grid1.getCharacterAtCoordinates(colB, rowA)
                newB = self._grid2.getCharacterAtCoordinates(colA, rowB)

            plainText.append(newA)
            plainText.append(newB)

        return plainText

    def getAdjacencyBonus(self):
        return self._grid1.getAdjacencyBonus() + self._grid2.getAdjacencyBonus()

