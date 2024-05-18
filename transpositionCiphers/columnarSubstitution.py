import random

class columnarSubstitution():

    def __init__(self,cipher):
        self.__cipher = cipher # the cipherText
        self.__length = len(self.__cipher)

        self.__maxKeyLength = int(self.__length**0.5)
        self.__setNewKeyLength(2)

    def shuffle(self):
        if random.random() > 0.5:
            self.__rollAmount = False
            self.__choices = random.sample(self.__key, k=2)
            self.__key[self.__choices[0]], self.__key[self.__choices[1]] = self.__key[self.__choices[1]], self.__key[self.__choices[0]]
        else:
            self.__rollAmount = random.randint(1, self.__keyLength - 1)
            self.__key = self.__key[self.__rollAmount:] + self.__key[:self.__rollAmount]

    def shake(self):
        if self.__keyLength <= self.__maxKeyLength:
            self.__setNewKeyLength(self.__keyLength+1)
        else:
            self.__setNewKeyLength(2)


    def undoShuffle(self):
        if self.__rollAmount:
            self.__key = self.__key[self.__keyLength - self.__rollAmount:] + self.__key[:self.__keyLength - self.__rollAmount]
        else:
            self.__key[self.__choices[0]], self.__key[self.__choices[1]] = self.__key[self.__choices[1]], self.__key[self.__choices[0]]
    
    def __setNewKeyLength(self,length):
        self.__keyLength = length
        self.__key = list(range(self.__keyLength))
        self.__numberOfFilledRows, self.__leftOver = divmod(self.__length, self.__keyLength)
    
    def decipher(self):
        # this decipher function is really efficient, at the cost of being really unreadable
        plainText = []

        orderedLongs = self.__key[:self.__leftOver]

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
            for column in self.__key:
                plainText.append(self.__cipher[lengthLeadingUpTo[column]+row])

        for column in orderedLongs:
            plainText.append(self.__cipher[lengthLeadingUpTo[column]+self.__numberOfFilledRows])

        return plainText
