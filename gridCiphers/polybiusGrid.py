import random
from copy import deepcopy

class polybiusGrid():

    # grid characters is a list of characters in rows and columns in the grid. Any of the following are valid grids:
    # ["abcde","fghik","lmnop","qrstu","vwxyz"] (typical polybius square using strings)
    # [[0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14],[15,16,17,18,19],[10,21,22,23,24]] (y and z are combined in an integer version)
    # ["abcde0","fghik1","lmnop2","qrstu3","vwxyz4"] (a rectangular grid with a few numbers)

    def __init__(self,gridCharacters = [[0,1,2,3,4],[5,6,7,8,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]):

        # default arguments are shared between instances.
        # If this deep copy weren't present every single polybius grid currently instantiated would share the same array
        self._grid = deepcopy(gridCharacters)

        self.__coordinates = []
        self._characterToCoordinates = {}
        for y,row in enumerate(gridCharacters):
            for x,character in enumerate(row):
                self._characterToCoordinates[character] = (x, y)
                self.__coordinates.append((x,y))

    def getCoordinatesOfCharacter(self,character):
        return self._characterToCoordinates[character]

    def getCharacterAtCoordinates(self,x,y):
        return self._grid[y][x]

    def getGrid(self):
        return self._grid

    # Fill row by row, left to right
    def fillHorizontally(self, character):
        index = 0
        for y in range(5):
            for x in range(5):
                self._grid[y][x] = character[index]
                self._characterToCoordinates[character[index]] = (x,y)
                index += 1

    # fill column by column, top to bottom
    def fillVertically(self, character):
        index = 0
        for x in range(5):
            for y in range(5):
                self._grid[y][x] = character[index]
                self._characterToCoordinates[character[index]] = (x,y)
                index += 1

    # start at top left and spiral inward CW
    def fillSpiralCW(self, character):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        x, y = 0, 0
        directionIndex = 0
        visited = set()

        for char in character:
            self._grid[y][x] = char
            self._characterToCoordinates[char] = (x, y)
            visited.add(x, y)

            nextX = x + directions[directionIndex][0]
            nextY = y + directions[directionIndex][1]

            # check if next cell is out of bounds or already visited
            if not (0 <= nextX < len(self._grid[0]) and 0 <= nextY < len(self._grid)) or (nextX, nextY) in visited:
                # change direction
                directionIndex = (directionIndex + 1) % 4
                nextX = x + directions[directionIndex][0]
                nextY = y + directions[directionIndex][1]

            x, y = nextX, nextY

    # start at top left and spiral inward CCW
    def fillSpiralCCW(self, character):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        x, y = 0, 0
        directionIndex = 0
        visited = set()

        for char in character:
            self._grid[y][x] = char
            self._characterToCoordinates[char] = (x, y)
            visited.add((x, y))

            nextX = x + directions[directionIndex][0]
            nextY = y + directions[directionIndex][1]

            # check if next cell is out of bounds or already visited
            if not (0 <= nextX < len(self._grid[0]) and 0 <= nextY < len(self._grid)) or (nextX, nextY) in visited:
                # change direction
                directionIndex = (directionIndex + 1) % 4
                nextX = x + directions[directionIndex][0]
                nextY = y + directions[directionIndex][1]

            x, y = nextX, nextY

    def test(self):
        for rowNum,row in enumerate(self._grid):
            for colNum,col in enumerate(row):
                if (colNum,rowNum) != self._characterToCoordinates[col]:
                    print("CRITICAL ERROR")
                    print(self._grid)
                    print(self._characterToCoordinates)
                    exit(1)

    def shuffle(self):

        self.__swappedCoordinates = random.sample(self.__coordinates,k=2)

        self.__firstCharacter = self.getCharacterAtCoordinates(self.__swappedCoordinates[0][0],self.__swappedCoordinates[0][1])
        self.__secondCharacter = self.getCharacterAtCoordinates(self.__swappedCoordinates[1][0],self.__swappedCoordinates[1][1])

        self._characterToCoordinates[self.__firstCharacter] = self.__swappedCoordinates[1]
        self._characterToCoordinates[self.__secondCharacter] = self.__swappedCoordinates[0]

        self._grid[self.__swappedCoordinates[0][1]][self.__swappedCoordinates[0][0]] = self.__secondCharacter
        self._grid[self.__swappedCoordinates[1][1]][self.__swappedCoordinates[1][0]] = self.__firstCharacter

    def undoShuffle(self):
        self._characterToCoordinates[self.__firstCharacter] = self.__swappedCoordinates[0]
        self._characterToCoordinates[self.__secondCharacter] = self.__swappedCoordinates[1]

        self._grid[self.__swappedCoordinates[0][1]][self.__swappedCoordinates[0][0]] = self.__firstCharacter
        self._grid[self.__swappedCoordinates[1][1]][self.__swappedCoordinates[1][0]] = self.__secondCharacter

    def getHorizontalAdjacencyBonus(self):
        horizontalAdjacencyBonus = 0
        previous = self._grid[0][0]

        for row in self._grid:
            for character in row:
                horizontalAdjacencyBonus += (character-previous)**2
                previous = character

        return -horizontalAdjacencyBonus

    def getVerticalAdjacencyBonus(self):
        verticalAdjacencyBonus = 0
        previous = self._grid[0][0]

        for column in range(len(self._grid[0])):
            for row in range(len(self._grid)):
                character = self._grid[row][column]
                verticalAdjacencyBonus += (character-previous)**2
                previous = character

        return -verticalAdjacencyBonus

    def getSpiralCWAdjacencyBonus(self):
        spiralAdjacencyBonusCW = 0
        directionsCW = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        x, y = 0, 0
        directionIndex = 0
        visited = set()
        visited.add((x, y))
        previous = self._grid[y][x]

        for _ in range(len(self._grid) * len(self._grid[0]) - 1):
            nextX = x + directionsCW[directionIndex][0]
            nextY = y + directionsCW[directionIndex][1]

            if not (0 <= nextX < len(self._grid[0]) and 0 <= nextY < len(self._grid)) or (nextX, nextY) in visited:
                directionIndex = (directionIndex + 1) % 4
                nextX = x + directionsCW[directionIndex][0]
                nextY = y + directionsCW[directionIndex][1]

            x, y = nextX, nextY
            current = self._grid[y][x]
            spiralAdjacencyBonusCW += (current-previous)**2
            previous = current
            visited.add((x, y))

        return -spiralAdjacencyBonusCW

    def getSpiralCCWAdjacencyBonus(self):
        spiralAdjacencyBonusCCW = 0
        directionsCCW = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        x, y = 0, 0
        directionIndex = 0
        visited = set()
        visited.add((x, y))
        previous = self._grid[y][x]

        for _ in range(len(self._grid) * len(self._grid[0]) - 1):
            nextX = x + directionsCCW[directionIndex][0]
            nextY = y + directionsCCW[directionIndex][1]

            if not (0 <= nextX < len(self._grid[0]) and 0 <= nextY < len(self._grid)) or (nextX, nextY) in visited:
                directionIndex = (directionIndex + 1) % 4
                nextX = x + directionsCCW[directionIndex][0]
                nextY = y + directionsCCW[directionIndex][1]

            x, y = nextX, nextY
            current = self._grid[y][x]
            spiralAdjacencyBonusCCW += (current-previous) **2
            previous = current
            visited.add((x, y))

        return -spiralAdjacencyBonusCCW

    def getAdjacencyBonus(self):
        return max(self.getHorizontalAdjacencyBonus(),
                   self.getVerticalAdjacencyBonus(),
                   self.getSpiralCCWAdjacencyBonus(),
                   self.getSpiralCWAdjacencyBonus()
                  )
