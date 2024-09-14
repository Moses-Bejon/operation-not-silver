# to be used in hill climb with margin with margin of 0.05*score and shuffle chance of 0.5
# requires custom string to int function due to presence of extra character
# (may need to be customised if that extra character is not "_")
# when evaluating, remove the extra character before you evaluate
# (e.g evaluateQuadgramFrequencies(list(filter((26).__ne__, plainText))))

from bifid import bifid
from polybiusCuboid import polybiusCuboid

def stringToInt(cipher):
    formattedCipher = []
    for letter in cipher:
        if letter.isalpha():
            formattedCipher.append(ord(letter.lower()) - 97)
        elif letter == "_":
            formattedCipher.append(26)
    return formattedCipher

class trifid(bifid):
    def __init__(self,cipher):
        super().__init__(cipher,polybiusCuboid)

    def decipher(self):

        plainText = []
        for fraction in self._fractions:
            coordinates = []

            for character in fraction:
                coordinateOfCharacter = self._key.getCoordinatesOfCharacter(character)
                coordinates.append(coordinateOfCharacter[2])
                coordinates.append(coordinateOfCharacter[1])
                coordinates.append(coordinateOfCharacter[0])

            for i in range(self._period):
                plainText.append(self._key.getCharacterAtCoordinates(coordinates[i + 2*self._period],coordinates[i + self._period], coordinates[i]))

        coordinates = []
        for character in self._lastFraction:
            coordinateOfCharacter = self._key.getCoordinatesOfCharacter(character)
            coordinates.append(coordinateOfCharacter[2])
            coordinates.append(coordinateOfCharacter[1])
            coordinates.append(coordinateOfCharacter[0])

        for i in range(self._lastFractionLength):
            plainText.append(
                self._key.getCharacterAtCoordinates(coordinates[i + 2*self._lastFractionLength],coordinates[i + self._lastFractionLength], coordinates[i]))

        return plainText
