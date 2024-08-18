from monoAlphaNumericSubstitution import monoAlphaNumericSubstitution
from columnarSubstitution import columnarSubstitution
from evaluate import getLetterAndNumberFrequencies,getIOC,getLetterAndNumberEntropy,normaliseLetterFrequencies
from ADFGX import ADFGX

class ADFGVX(ADFGX):
    def __init__(self,cipher,transpositionCipher=columnarSubstitution):
        super().__init__(cipher,transpositionCipher)

    def formatCipher(self,cipher):
        formattedCipher = []
        for character in cipher:
            match character:
                case "A" | "a":
                    formattedCipher.append(0)
                case "D" | "d":
                    formattedCipher.append(1)
                case "F" | "f":
                    formattedCipher.append(2)
                case "G" | "g":
                    formattedCipher.append(3)
                case "V" | "v":
                    formattedCipher.append(4)
                case "X" | "x":
                    formattedCipher.append(5)

        return formattedCipher

    def polybiusify(self,transposedText):
        polybiusified = []

        for i in range(0, self._length, 2):
            polybiusified.append(transposedText[i] * 6 + transposedText[i + 1])

        return polybiusified

    def keyFinderEvaluator(self, transposedText):
        polybiusified = self.polybiusify(transposedText)

        frequencies,total = getLetterAndNumberFrequencies(polybiusified)

        emptySpots = 0
        for frequency in frequencies:
            if frequency == 0:
                emptySpots += 1

        return getIOC(frequencies,total)*getLetterAndNumberEntropy(normaliseLetterFrequencies(frequencies,total))*emptySpots

    def shake(self):
        self._place += 1
        self._cipher = monoAlphaNumericSubstitution(self._cipherCandidates[self._place % self._numberOfCandidates])