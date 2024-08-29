# to be run in hill climb with shake threshold of 5000 and shake amount of 10

from monoAlphabeticSubstitution import monoAlphabeticSubstitution
from columnarSubstitution import columnarSubstitution
from evaluate import getLetterFrequencies,getIOC,getEntropy,normaliseLetterFrequencies
from hillClimbKeyFinder import hillClimbKeyFinder
from polybiusSquare import formatPolybius

# to be used in hill
class ADFGX():
    def __init__(self,cipher,transpositionCipher=columnarSubstitution):
        formattedCipher = self.formatCipher(cipher)
        self._length = len(self.formatCipher(cipher))

        self.__transpositionCipher = transpositionCipher(formattedCipher)

        # as this function takes a while, alerting the user I am at work and nothing is wrong
        print("I have started looking for potential keys for the transposition portion of the cipher")
        keys = hillClimbKeyFinder(self.__transpositionCipher, self.keyFinderEvaluator, 100000, 30)
        print("I have found the following keys with the following scores: ",keys)

        self.setKeyCandidates(keys[0][::-1])

    def formatCipher(self,cipher):
        formattedCipher = formatPolybius(cipher,["a","d","f","g","x"])
        if not formattedCipher:
            formattedCipher = formatPolybius(cipher,["A","D","F","G","X"])

        return formattedCipher

    def keyFinderEvaluator(self, transposedText):
        polybiusified = self.polybiusify(transposedText)

        letterFrequencies,total = getLetterFrequencies(polybiusified)

        return getIOC(letterFrequencies,total)*getEntropy(normaliseLetterFrequencies(letterFrequencies,total))

    def polybiusify(self,transposedText):
        polybiusified = []

        for i in range(0, self._length, 2):
            polybiusified.append(transposedText[i] * 5 + transposedText[i + 1])

        return polybiusified

    def setKeyCandidates(self,keyCandidates):
        self._cipherCandidates = []
        self._numberOfCandidates = len(keyCandidates)

        for key in keyCandidates:
            self.__transpositionCipher.injectKey(key)
            self._cipherCandidates.append(self.polybiusify(self.__transpositionCipher.decipher()))

        self._place = -1
        self.shake()

    def shake(self):
        self._place += 1
        self._cipher = monoAlphabeticSubstitution(self._cipherCandidates[self._place % self._numberOfCandidates])

    def shuffle(self):
        self._cipher.shuffle()

    def undoShuffle(self):
        self._cipher.undoShuffle()

    def decipher(self):
        return self._cipher.decipher()
