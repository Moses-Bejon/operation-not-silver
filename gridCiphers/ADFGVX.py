# to be run in hill climb with shake threshold of 5000 and shake amount of 10
# you need to use the alphanumeric evaluator to evaluate the produced plain texts

from monoAlphaNumericSubstitution import monoAlphaNumericSubstitution
from columnarSubstitution import columnarSubstitution
from evaluate import getLetterAndNumberFrequencies,getIOC,getLetterAndNumberEntropy,normaliseLetterFrequencies
from ADFGX import ADFGX
from polybiusSquare import formatPolybius

class ADFGVX(ADFGX):
    def __init__(self,cipher,transpositionCipher=columnarSubstitution):
        super().__init__(cipher,transpositionCipher)

    def formatCipher(self,cipher):
        formattedCipher = formatPolybius(cipher,["a","d","f","g","v","x"])
        if not formattedCipher:
            formattedCipher = formatPolybius(cipher,["A","D","F","G","V","X"])

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
