from monoAlphabeticSubstitution import monoAlphabeticSubstitution
from evaluate import getLetterFrequencies,getIOC,getEntropy,normaliseLetterFrequencies
from hillClimbKeyFinder import hillClimbKeyFinder

class ADFGX():
    def __init__(self,cipher,transpositionCipher):
        formattedCipher = self.formatCipher(cipher)
        self.__length = len(self.formatCipher(cipher))

        self.__transpositionCipher = transpositionCipher(formattedCipher)

        # as this function takes a while, alerting the user I am at work and nothing is wrong
        print("I have started looking for potential keys for the transposition portion of the cipher")
        keys = hillClimbKeyFinder(self.__transpositionCipher, self.keyFinderEvaluator, 100000, 20)
        print("I have found the following keys with the following scores: ",keys)

        self.setKeyCandidates(keys[0])

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
                case "X" | "x":
                    formattedCipher.append(4)

        return formattedCipher

    def keyFinderEvaluator(self, transposedText):
        polybiusified = self.polybiusify(transposedText)

        letterFrequencies,total = getLetterFrequencies(polybiusified)

        return getIOC(letterFrequencies,total)*getEntropy(normaliseLetterFrequencies(letterFrequencies,total))

    def polybiusify(self,transposedText):
        polybiusified = []

        for i in range(0, self.__length, 2):
            polybiusified.append(transposedText[i] * 5 + transposedText[i + 1])

        return polybiusified

    def setKeyCandidates(self,keyCandidates):
        self.__cipherCandidates = []
        self.__numberOfCandidates = len(keyCandidates)

        for key in keyCandidates:
            self.__transpositionCipher.injectKey(key)
            self.__cipherCandidates.append(self.polybiusify(self.__transpositionCipher.decipher()))

        self.__place = -1
        self.shake()

    def shake(self):
        self.__place += 1
        self.__cipher = monoAlphabeticSubstitution(self.__cipherCandidates[self.__place%self.__numberOfCandidates])

    def shuffle(self):
        self.__cipher.shuffle()

    def undoShuffle(self):
        self.__cipher.undoShuffle()

    def decipher(self):
        return self.__cipher.decipher()