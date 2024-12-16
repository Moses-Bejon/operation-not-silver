import random
class monoAlphabeticSubstitution():
    def __init__(self,cipher):
        self.__cipher = cipher
        self._key = {}
        for i in range(26):
            self._key[i] = i

    def printKey(self):
        print(self._key)

    def getKey(self):
        return self._key

    def getNumberOfKeys(self):
        return 1

    def injectKey(self,key):
        self._key = key

    def shuffle(self):
        self._letters = random.sample(range(26), k=2)
        self._key[self._letters[0]],self._key[self._letters[1]] = self._key[self._letters[1]],self._key[self._letters[0]]

    def undoShuffle(self):
        self._key[self._letters[0]],self._key[self._letters[1]] = self._key[self._letters[1]],self._key[self._letters[0]]

    def decipher(self):
        plainText = []
        for letter in self.__cipher:
            plainText.append(self._key[letter])
        return plainText
