# To be run in hillClimbWithMargin. Optimal conditions: margin = 0.1*length Chance to shuffle = 0.5

from verticalTwoSquare import verticalTwoSquare
from polybiusGrid import polybiusGrid

class fourSquare(verticalTwoSquare):
    def __init__(self,cipher):
        super().__init__(cipher)
        self.__readingOffGrid = polybiusGrid()

    def decipher(self):
        plainText = []

        for i in range(self._halfLength):
            coordinate1 = self._grid1.getCoordinatesOfCharacter(self._cipher[i * 2])
            coordinate2 = self._grid2.getCoordinatesOfCharacter(self._cipher[i * 2 + 1])

            plainText.append(
                self.__readingOffGrid.getCharacterAtCoordinates(coordinate2[1],coordinate1[0])
            )

            plainText.append(
                self.__readingOffGrid.getCharacterAtCoordinates(coordinate1[1],coordinate2[0])
            )

        return plainText
