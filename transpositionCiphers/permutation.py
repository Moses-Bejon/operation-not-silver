import random

class permutation(): # also name the file the same way please

    def __init__(self,cipher):
        self.__cipher = cipher # the cipherText

        length = len(self.__cipher)

        # length of key is a factor of the length of the cipher text
        self.__keyLengths = []

        for possibleFactor in range(2,int(length ** 0.5)):
            if length % possibleFactor == 0:
                self.__keyLengths.append(possibleFactor)

        self.__keyLength = random.choice(self.__keyLengths)
        self.__key = list(range(self.__keyLength))


    def shuffle(self):
        if random.random()>0.5:
            self.__rollAmount = False
            self.__choices = random.sample(self.__key,k=2)
            self.__key[self.__choices[0]],self.__key[self.__choices[1]]=self.__key[self.__choices[1]],self.__key[self.__choices[0]]
        else:
            self.__rollAmount = random.randint(1, self.__keyLength - 1)
            self.__key = self.__key[self.__rollAmount:] + self.__key[:self.__rollAmount]
    def shake(self):
        self.__keyLength = random.choice(self.__keyLengths)
        self.__key = list(range(self.__keyLength))

    def undoShuffle(self):
        if self.__rollAmount:
            self.__key = self.__key[self.__keyLength - self.__rollAmount:] + self.__key[:self.__keyLength - self.__rollAmount]
        else:
            self.__key[self.__choices[0]], self.__key[self.__choices[1]] = self.__key[self.__choices[1]], self.__key[self.__choices[0]]
    def decipher(self):
        plainText = ""
        for place in range(0, len(self.__cipher), self.__keyLength):
            row = self.__cipher[place:place + self.__keyLength]
            for value in self.__key:
                plainText += row[value]
        return plainText


