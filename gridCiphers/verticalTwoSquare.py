# To be run in hillClimbWithMargin. Optimal conditions: margin = 0.1*length Chance to shuffle = 0.5

import random
from polybiusGrid import polybiusGrid

class verticalTwoSquare():
    def __init__(self,cipher):
        self._cipher = cipher

        self._halfLength = round(len(self._cipher)/2)

        self._grid1 = polybiusGrid([[0,1,2,3,4],[5,6,7,8,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]])
        self._grid2 = polybiusGrid([[0,1,2,3,4],[5,6,7,8,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]])

    def shuffle(self):
        if random.random() > 0.5:
            self.__shuffledGrid1 = True
            self._grid1.shuffle()
        else:
            self.__shuffledGrid1 = False
            self._grid2.shuffle()

    def undoShuffle(self):
        if self.__shuffledGrid1:
            self._grid1.undoShuffle()
        else:
            self._grid2.undoShuffle()

    def decipher(self):

        plainText = []

        for i in range(self._halfLength):
            coordinate1 = self._grid1.getCoordinatesOfCharacter(self._cipher[i*2])
            coordinate2 = self._grid2.getCoordinatesOfCharacter(self._cipher[i*2+1])

            plainText.append(self._grid1.getCharacterAtCoordinates(coordinate2[0],coordinate1[1]))
            plainText.append(self._grid2.getCharacterAtCoordinates(coordinate1[0],coordinate2[1]))

        return plainText
