from permutationKey import permutationKey

class permutation():

    def __init__(self,cipher):
        self.__cipher = cipher # the cipherText

        length = len(self.__cipher)

        # length of key is a factor of the length of the cipher text
        keyLengths = []

        for possibleFactor in range(2,int(length ** 0.5)+1):
            if length % possibleFactor == 0:
                keyLengths.append(possibleFactor)

        self.__key = permutationKey(keyLengths)


    def shuffle(self):
        self.__key.shuffle()

    def shake(self):
        self.__key.shake()

    def undoShuffle(self):
        self.__key.undoShuffle()

    def decipher(self):

        key = self.__key.getKey()
        keyLength = self.__key.getLength()

        plainText = []
        for place in range(0, len(self.__cipher), keyLength):
            row = self.__cipher[place:place + keyLength]
            for value in key:
                plainText.append(row[value])
        return plainText

    def getKey(self):
        return self.__key.getKey()

    def injectKey(self,key):
        self.__key.injectKey(key)
