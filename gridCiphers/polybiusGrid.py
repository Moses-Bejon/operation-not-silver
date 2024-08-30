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
        self.__grid = deepcopy(gridCharacters)

        self.__coordinates = []
        self.__characterToCoordinates = {}
        for y,row in enumerate(gridCharacters):
            for x,character in enumerate(row):
                self.__characterToCoordinates[character] = (x,y)
                self.__coordinates.append((x,y))

    def getCoordinatesOfCharacter(self,character):
        return self.__characterToCoordinates[character]

    def getCharacterAtCoordinates(self,x,y):
        return self.__grid[y][x]

    def shuffle(self):

        self.__swappedCoordinates = random.sample(self.__coordinates,k=2)

        self.__firstCharacter = self.getCharacterAtCoordinates(self.__swappedCoordinates[0][0],self.__swappedCoordinates[0][1])
        self.__secondCharacter = self.getCharacterAtCoordinates(self.__swappedCoordinates[1][0],self.__swappedCoordinates[1][1])

        self.__characterToCoordinates[self.__firstCharacter] = self.__swappedCoordinates[1]
        self.__characterToCoordinates[self.__secondCharacter] = self.__swappedCoordinates[0]

        self.__grid[self.__swappedCoordinates[0][1]][self.__swappedCoordinates[0][0]] = self.__secondCharacter
        self.__grid[self.__swappedCoordinates[1][1]][self.__swappedCoordinates[1][0]] = self.__firstCharacter

    def undoShuffle(self):
        self.__characterToCoordinates[self.__firstCharacter] = self.__swappedCoordinates[0]
        self.__characterToCoordinates[self.__secondCharacter] = self.__swappedCoordinates[1]

        self.__grid[self.__swappedCoordinates[0][1]][self.__swappedCoordinates[0][0]] = self.__firstCharacter
        self.__grid[self.__swappedCoordinates[1][1]][self.__swappedCoordinates[1][0]] = self.__secondCharacter