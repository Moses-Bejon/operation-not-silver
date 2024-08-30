# to be used in hill climb with shake threshold of 5000 and shake amount of 10

from monoAlphabeticSubstitution import monoAlphabeticSubstitution

# key invalid is the exception the code will call if it suddenly discovers a given key is invalid
class KeyInvalid(Exception):
    pass

class nihilist():

    def __init__(self,
                 cipher,
                 cipherGrid = [[11,12,13,14,15],[21,22,23,24,25],[31,32,33,34,35],[41,42,43,44,45],[51,52,53,54,55]],
                 translatedGrid = [[0,1,2,3,4],[5,6,7,8,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]],
                 finalCipherType = monoAlphabeticSubstitution
                 ):

        self.__finalCipherType = finalCipherType

        self.__minGridVal = cipherGrid[0][0]
        self.__gridRange = cipherGrid[-1][-1]-self.__minGridVal

        self.__cipher = []

        currentNumber = ""
        for character in cipher:
            if character.isdigit():
                currentNumber += character
            else:
                if currentNumber:
                    character = int(currentNumber)
                    if character < self.__minGridVal:
                        character += 100

                    self.__cipher.append(character)
                    currentNumber = ""
        self.__length = len(self.__cipher)

        self.__cipherGridValueToTranslatedGridValue = {}

        for i in range(len(cipherGrid)):
            for j in range(len(cipherGrid[0])):
                self.__cipherGridValueToTranslatedGridValue[cipherGrid[i][j]] = translatedGrid[i][j]

        self.__possibleMonoAlphabeticCiphers = []

        for keyLength in range(1, int(len(self.__cipher) ** 0.5) + 1):

            try:
                slicePossibilities = [[]] * keyLength

                for slice in range(keyLength):

                    maximum = minimum = self.__cipher[slice]

                    for i in range(slice, self.__length, keyLength):

                        character = self.__cipher[i]

                        if character < minimum:
                            if maximum - character > self.__gridRange:
                                raise KeyInvalid

                            minimum = character

                        elif character > maximum:
                            if character - minimum > self.__gridRange:
                                raise KeyInvalid
                            maximum = character

                    possibleOffsets = []

                    sliceRange = maximum - minimum

                    for i in range(self.__gridRange - sliceRange + 1):
                        possibleOffsets.append(minimum - self.__minGridVal + i)

                    slicePossibilities[slice] = possibleOffsets

                monoAlphabeticCipher = [0] * self.__length

                self.tryAllOffsets(slicePossibilities, 0, monoAlphabeticCipher, keyLength)

            except KeyInvalid:
                pass

        self.__place = -1
        self.__numberOfCandidates = len(self.__possibleMonoAlphabeticCiphers)
        if not self.__numberOfCandidates:
            print("this cipher text either is not a nihilist cipher or is a nihilist cipher on different settings as those input")

        self.shake()

    def tryAllOffsets(self,slicePossibilities, slice, plainText,keyLength):

        nextSlice = slice + 1
        lastSlice = nextSlice == len(slicePossibilities)

        for offset in slicePossibilities[slice]:
            for i in range(slice, self.__length, keyLength):
                try:
                    plainText[i] = self.__cipherGridValueToTranslatedGridValue[self.__cipher[i] - offset]
                except KeyError:
                    break
            else:
                if lastSlice:
                    self.__possibleMonoAlphabeticCiphers.append(plainText.copy())
                else:
                    self.tryAllOffsets(slicePossibilities, nextSlice, plainText, keyLength)

    def shake(self):
        self.__place += 1
        self.__cipher = self.__finalCipherType(self.__possibleMonoAlphabeticCiphers[self.__place%self.__numberOfCandidates])

    def shuffle(self):
        self.__cipher.shuffle()

    def undoShuffle(self):
        self.__cipher.undoShuffle()

    def decipher(self):
        return self.__cipher.decipher()
