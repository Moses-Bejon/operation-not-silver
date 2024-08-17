from permutationKey import permutationKey
import random

class columnarSubstitution():

    def __init__(self,cipher):
        self.__cipher = cipher
        self.__length = len(self.__cipher)

        self.__key = permutationKey(range(2,int(self.__length**0.5)+1))
        self.updateKeyLength()

    def shuffle(self):
        self.__key.shuffle()

    def shake(self):
        if random.random() > 0.5:
            self.__key.shake()
            self.updateKeyLength()
        else:
            for _ in range(3):
                self.__key.shuffle()

    def updateKeyLength(self):
        self.__keyLength = self.__key.getLength()
        self.__numberOfFilledRows, self.__leftOver = divmod(self.__length, self.__keyLength)

    def undoShuffle(self):
        self.__key.undoShuffle()

    def getKey(self):
        return self.__key.getKey()

    def decipher(self):
        # this decipher function is really efficient, at the cost of being really unreadable
        plainText = []

        key = self.__key.getKey()

        orderedLongs = key[:self.__leftOver]

        lengthLeadingUpTo = {0: 0}
        longNumbers = set(orderedLongs)
        place = 0
        for i in range(1,self.__keyLength):
            if i-1 in longNumbers:
                place += self.__numberOfFilledRows + 1
            else:
                place += self.__numberOfFilledRows
            lengthLeadingUpTo[i] = place

        for row in range(self.__numberOfFilledRows):
            for column in key:
                plainText.append(self.__cipher[lengthLeadingUpTo[column]+row])

        for column in orderedLongs:
            plainText.append(self.__cipher[lengthLeadingUpTo[column]+self.__numberOfFilledRows])

        return plainText

    def injectKey(self,key):
        self.__key.injectKey(key)
        self.updateKeyLength()
