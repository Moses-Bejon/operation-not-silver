import random

from polybiusGrid import polybiusGrid

class polybiusGridEnhancedShuffle(polybiusGrid):
    def __init__(self,gridCharacters = [[0,1,2,3,4],[5,6,7,8,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]):
        super().__init__(gridCharacters)

    def shuffle(self):
        self.test()
        randomNum = random.random()

        if randomNum < 0.9:
            self.__shuffleMode = 0
            super().shuffle()
        elif randomNum < 0.95:
            self.__shuffleMode = 1
            self.swapRows()
        else:
            self.__shuffleMode = 2
            self.swapColumns()
        self.test()

    def swapRows(self):
        self.__swap = random.sample(range(5), 2)

        rowA, rowB = self.__swap
        self._grid[rowA], self._grid[rowB] = self._grid[rowB], self._grid[rowA]

        for x in range(5):
            self._characterToCoordinates[self._grid[rowA][x]] = (x,rowA)
            self._characterToCoordinates[self._grid[rowB][x]] = (x,rowB)

    def swapColumns(self):
        self.__swap = random.sample(range(5), 2)
        colA, colB = self.__swap
        for y in range(5):
            self._grid[y][colA], self._grid[y][colB] = self._grid[y][colB], self._grid[y][colA]
            self._characterToCoordinates[self._grid[y][colA]] = (colA,y)
            self._characterToCoordinates[self._grid[y][colB]] = (colB,y)

    def undoSwapColumns(self):
        colA, colB = self.__swap
        for y in range(5):
            self._grid[y][colA], self._grid[y][colB] = self._grid[y][colB], self._grid[y][colA]
            self._characterToCoordinates[self._grid[y][colA]] = (colA, y)
            self._characterToCoordinates[self._grid[y][colB]] = (colB, y)

    def undoSwapRows(self):
        rowA, rowB = self.__swap
        self._grid[rowA], self._grid[rowB] = self._grid[rowB], self._grid[rowA]

        for x in range(5):
            self._characterToCoordinates[self._grid[rowA][x]] = (x, rowA)
            self._characterToCoordinates[self._grid[rowB][x]] = (x, rowB)

    def undoShuffle(self):
        self.test()
        match self.__shuffleMode:
            case 0:
                super().undoShuffle()
            case 1:
                self.undoSwapRows()
            case 2:
                self.undoSwapColumns()
        self.test()