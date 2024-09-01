# to be run in hillClimbWithMargin
# optimal conditions:
# margin: length*0.2
# chance to shuffle: 0.5

from polybiusGridEnhancedShuffle import polybiusGridEnhancedShuffle
from evaluate import getLetterFrequencies,getIOC

class bifid():

    def __init__(self,cipher):
        self.__cipher = cipher
        self.__length = len(self.__cipher)
        self.__key = polybiusGridEnhancedShuffle()

        bestIOC = 0
        bestPeriod = 0
        for possiblePeriod in range(2,len(self.__cipher)):
            self.setPeriod(possiblePeriod)
            IOC = getIOC(*getLetterFrequencies(self.decipher()))

            if IOC > bestIOC:
                bestIOC = IOC
                bestPeriod = possiblePeriod

        if bestPeriod > 20:
            bestPeriod = len(self.__cipher)
        self.setPeriod(bestPeriod)
        print("using period",bestPeriod)

    def setPeriod(self,period):
        self.__period = period

        self.__fractions = []
        for i in range(period,self.__length,period):
            self.__fractions.append(self.__cipher[i-period:i])

        self.__lastFractionLength = self.__length%period

        self.__lastFraction = self.__cipher[-self.__lastFractionLength:]

        if self.__lastFractionLength == 0:
            self.__lastFractionLength = period

    def decipher(self):

        plainText = []
        for fraction in self.__fractions:
            coordinates = []

            for character in fraction:
                coordinateOfCharacter = self.__key.getCoordinatesOfCharacter(character)
                coordinates.append(coordinateOfCharacter[1])
                coordinates.append(coordinateOfCharacter[0])

            for i in range(self.__period):
                plainText.append(self.__key.getCharacterAtCoordinates(coordinates[i + self.__period], coordinates[i]))

        coordinates = []
        for character in self.__lastFraction:
            coordinateOfCharacter = self.__key.getCoordinatesOfCharacter(character)
            coordinates.append(coordinateOfCharacter[1])
            coordinates.append(coordinateOfCharacter[0])

        for i in range(self.__lastFractionLength):
            plainText.append(self.__key.getCharacterAtCoordinates(coordinates[i + self.__lastFractionLength], coordinates[i]))

        return plainText

    def shuffle(self):
        self.__key.shuffle()

    def undoShuffle(self):
        self.__key.undoShuffle()
