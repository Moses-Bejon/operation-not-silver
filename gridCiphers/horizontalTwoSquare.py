# To be run in hillClimbWithMargin. Optimal conditions: margin = 0.1*length Chance to shuffle = 0.5

from verticalTwoSquare import verticalTwoSquare

class horizontalTwoSquare(verticalTwoSquare):
    def __init__(self,cipher):
        super().__init__(cipher)

    def decipher(self):
        plainText = []

        for i in range(self._halfLength):
            coordinate1 = self._grid1.getCoordinatesOfCharacter(self._cipher[i * 2])
            coordinate2 = self._grid2.getCoordinatesOfCharacter(self._cipher[i * 2 + 1])

            plainText.append(self._grid2.getCharacterAtCoordinates(coordinate2[0], coordinate1[1]))
            plainText.append(self._grid1.getCharacterAtCoordinates(coordinate1[0], coordinate2[1]))

        return plainText
