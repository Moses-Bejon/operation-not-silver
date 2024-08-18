import random

class permutationKey():

    def __init__(self,possibleKeyLengths):
        self.__possibleKeyLengths = possibleKeyLengths
        self.__place = -1
        self.__numberOfPossibleKeyLengths = len(self.__possibleKeyLengths)
        self.shake()

    def shuffle(self):
        if random.random()>0.5:
            self.__rollAmount = False
            self.__choices = random.sample(self.__key,k=2)
            self.__key[self.__choices[0]],self.__key[self.__choices[1]]=self.__key[self.__choices[1]],self.__key[self.__choices[0]]
        else:
            self.__rollAmount = random.randint(1, self.__keyLength - 1)
            self.__key = self.__key[self.__rollAmount:] + self.__key[:self.__rollAmount]

    def undoShuffle(self):
        if self.__rollAmount:
            self.__key = self.__key[self.__keyLength - self.__rollAmount:] + self.__key[:self.__keyLength - self.__rollAmount]
        else:
            self.__key[self.__choices[0]], self.__key[self.__choices[1]] = self.__key[self.__choices[1]], self.__key[self.__choices[0]]

    def shake(self):

        self.__place += 1

        self.__keyLength = self.__possibleKeyLengths[self.__place%self.__numberOfPossibleKeyLengths]
        self.__key = list(range(self.__keyLength))

    def getKey(self):
        return self.__key

    def getLength(self):
        return self.__keyLength

    def injectKey(self,key):
        self.__key = key
        self.__keyLength = len(self.__key)

    def getNumberOfKeys(self):
        return self.__numberOfPossibleKeyLengths
