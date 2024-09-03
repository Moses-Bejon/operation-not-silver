import random
from copy import deepcopy

# operates similarly to polybiusGrid but is generalised to 3 dimensions

class polybiusCuboid():
    def __init__(self,gridCharacters=[[[0,1,2],[3,4,5],[6,7,8]],[[9,10,11],[12,13,14],[15,16,17]],[[18,19,20],[21,22,23],[24,25,26]]]):

        # default arguments are shared between instances.
        # If this deep copy weren't present every single polybius grid currently instantiated would share the same array
        self._cuboid = deepcopy(gridCharacters)

        self.__coordinates = []
        self._characterToCoordinates = {}
        for z,grid in enumerate(self._cuboid):
            for y, row in enumerate(grid):
                for x, character in enumerate(row):
                    self._characterToCoordinates[character] = (x, y, z)
                    self.__coordinates.append((x, y, z))

    def getCoordinatesOfCharacter(self, character):
        return self._characterToCoordinates[character]

    def getCharacterAtCoordinates(self,x,y,z):
        return self._cuboid[z][y][x]

    def test(self):
        for z,grid in enumerate(self._cuboid):
            for rowNum,row in enumerate(grid):
                for colNum,col in enumerate(row):
                    if (colNum,rowNum,z) != self._characterToCoordinates[col]:
                        print("CRITICAL ERROR")
                        print(self._cuboid)
                        print(self._characterToCoordinates)
                        exit(1)

    def shuffle(self):
        randomNum = random.random()

        if randomNum < 0.85:
            self.swapElements()
            self.__shuffleMode = 0
        elif randomNum < 0.9:
            self.swapXPlanes()
            self.__shuffleMode = 1
        elif randomNum < 0.95:
            self.swapYPlanes()
            self.__shuffleMode = 2
        else:
            self.swapZPlanes()
            self.__shuffleMode = 3

    def undoShuffle(self):
        match self.__shuffleMode:
            case 0:
                self.undoElementSwap()
            case 1:
                self.undoSwapXPlanes()
            case 2:
                self.undoSwapYPlanes()
            case 3:
                self.undoSwapZPlanes()

    def swapElements(self):
        self.__swappedCoordinates = random.sample(self.__coordinates, k=2)

        self.__firstCharacter = self.getCharacterAtCoordinates(self.__swappedCoordinates[0][0],self.__swappedCoordinates[0][1],self.__swappedCoordinates[0][2])
        self.__secondCharacter = self.getCharacterAtCoordinates(self.__swappedCoordinates[1][0],self.__swappedCoordinates[1][1],self.__swappedCoordinates[1][2])

        self._characterToCoordinates[self.__firstCharacter] = self.__swappedCoordinates[1]
        self._characterToCoordinates[self.__secondCharacter] = self.__swappedCoordinates[0]

        self._cuboid[self.__swappedCoordinates[0][2]][self.__swappedCoordinates[0][1]][self.__swappedCoordinates[0][0]] = self.__secondCharacter
        self._cuboid[self.__swappedCoordinates[1][2]][self.__swappedCoordinates[1][1]][self.__swappedCoordinates[1][0]] = self.__firstCharacter

    def swapZPlanes(self):
        self.__swappedPlanes = random.sample(range(len(self._cuboid)),k=2)

        planeOne,planeTwo = self.__swappedPlanes

        self._cuboid[planeOne],self._cuboid[planeTwo] = self._cuboid[planeTwo],self._cuboid[planeOne]

        for y in range(len(self._cuboid[0])):
            for x in range(len(self._cuboid[0][0])):
                self._characterToCoordinates[self._cuboid[planeOne][y][x]] = (x,y,planeOne)
                self._characterToCoordinates[self._cuboid[planeTwo][y][x]] = (x, y, planeTwo)

    def swapYPlanes(self):
        self.__swappedPlanes = random.sample(range(len(self._cuboid[0])),k=2)

        planeOne,planeTwo = self.__swappedPlanes

        for z in range(len(self._cuboid)):
            self._cuboid[z][planeOne],self._cuboid[z][planeTwo] = self._cuboid[z][planeTwo],self._cuboid[z][planeOne]
            for x in range(len(self._cuboid[0])):
                self._characterToCoordinates[self._cuboid[z][planeOne][x]] = (x,planeOne,z)
                self._characterToCoordinates[self._cuboid[z][planeTwo][x]] = (x,planeTwo,z)

    def swapXPlanes(self):
        self.__swappedPlanes = random.sample(range(len(self._cuboid[0][0])),k=2)

        planeOne,planeTwo = self.__swappedPlanes

        for z in range(len(self._cuboid)):
            for y in range(len(self._cuboid[0])):
                self._cuboid[z][y][planeOne],self._cuboid[z][y][planeTwo] = self._cuboid[z][y][planeTwo],self._cuboid[z][y][planeOne]

                self._characterToCoordinates[self._cuboid[z][y][planeOne]] = (planeOne,y,z)
                self._characterToCoordinates[self._cuboid[z][y][planeTwo]] = (planeTwo,y,z)

    def undoSwapXPlanes(self):
        planeOne, planeTwo = self.__swappedPlanes

        for z in range(len(self._cuboid)):
            for y in range(len(self._cuboid[0])):
                self._cuboid[z][y][planeOne], self._cuboid[z][y][planeTwo] = self._cuboid[z][y][planeTwo], \
                self._cuboid[z][y][planeOne]

                self._characterToCoordinates[self._cuboid[z][y][planeOne]] = (planeOne, y, z)
                self._characterToCoordinates[self._cuboid[z][y][planeTwo]] = (planeTwo, y, z)

    def undoSwapYPlanes(self):


        planeOne, planeTwo = self.__swappedPlanes

        for z in range(len(self._cuboid)):
            self._cuboid[z][planeOne],self._cuboid[z][planeTwo] = self._cuboid[z][planeTwo],self._cuboid[z][planeOne]
            for x in range(len(self._cuboid[0])):
                self._characterToCoordinates[self._cuboid[z][planeOne][x]] = (x, planeOne, z)
                self._characterToCoordinates[self._cuboid[z][planeTwo][x]] = (x, planeTwo, z)

    def undoSwapZPlanes(self):
        planeOne,planeTwo = self.__swappedPlanes

        self._cuboid[planeOne], self._cuboid[planeTwo] = self._cuboid[planeTwo], self._cuboid[planeOne]

        for y in range(len(self._cuboid[0])):
            for x in range(len(self._cuboid[0][0])):
                self._characterToCoordinates[self._cuboid[planeOne][y][x]] = (x, y, planeOne)
                self._characterToCoordinates[self._cuboid[planeTwo][y][x]] = (x, y, planeTwo)

    def undoElementSwap(self):
        self._characterToCoordinates[self.__firstCharacter] = self.__swappedCoordinates[0]
        self._characterToCoordinates[self.__secondCharacter] = self.__swappedCoordinates[1]

        self._cuboid[self.__swappedCoordinates[0][2]][self.__swappedCoordinates[0][1]][self.__swappedCoordinates[0][0]] = self.__firstCharacter
        self._cuboid[self.__swappedCoordinates[1][2]][self.__swappedCoordinates[1][1]][self.__swappedCoordinates[1][0]] = self.__secondCharacter
