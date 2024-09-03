# to be run in hillClimbWithMargin
# optimal conditions:
# margin: length*0.2
# chance to shuffle: 0.5

from polybiusGrid import polybiusGrid
from evaluate import getLetterFrequenciesForAnyNumberOfCharacters,getIOC

class bifid():

    def __init__(self,cipher,key=polybiusGrid):
        self._cipher = cipher
        self._length = len(self._cipher)

        self._key = key()

        bestIOC = 0
        bestPeriod = 0
        for possiblePeriod in range(2, min(len(self._cipher),100)):
            self.setPeriod(possiblePeriod)
            IOC = getIOC(*getLetterFrequenciesForAnyNumberOfCharacters(self.decipher()))

            if IOC > bestIOC:
                bestIOC = IOC
                bestPeriod = possiblePeriod

        if bestPeriod > 20:
            bestPeriod = len(self._cipher)
        self.setPeriod(bestPeriod)
        print("using period",bestPeriod)

    def setPeriod(self,period):
        self._period = period

        self._fractions = []
        for i in range(period, self._length, period):
            self._fractions.append(self._cipher[i - period:i])

        self._lastFractionLength = self._length % period

        self._lastFraction = self._cipher[-self._lastFractionLength:]

        if self._lastFractionLength == 0:
            self._lastFractionLength = period

    def decipher(self):

        plainText = []
        for fraction in self._fractions:
            coordinates = []

            for character in fraction:
                coordinateOfCharacter = self._key.getCoordinatesOfCharacter(character)
                coordinates.append(coordinateOfCharacter[1])
                coordinates.append(coordinateOfCharacter[0])

            for i in range(self._period):
                plainText.append(self._key.getCharacterAtCoordinates(coordinates[i + self._period], coordinates[i]))

        coordinates = []
        for character in self._lastFraction:
            coordinateOfCharacter = self._key.getCoordinatesOfCharacter(character)
            coordinates.append(coordinateOfCharacter[1])
            coordinates.append(coordinateOfCharacter[0])

        for i in range(self._lastFractionLength):
            plainText.append(self._key.getCharacterAtCoordinates(coordinates[i + self._lastFractionLength], coordinates[i]))

        return plainText

    def shuffle(self):
        self._key.shuffle()

    def undoShuffle(self):
        self._key.undoShuffle()
