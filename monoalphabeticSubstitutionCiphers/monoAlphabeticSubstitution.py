import random
class monoAlphabeticSubstitution():
    def __init__(self,cipher):
        self.__cipher = cipher
        self.__key = {}
        for i in range(26):
            self.__key[i] = i

    def shuffle(self):
        self.__letters = random.sample(range(26),k=2)
        self.__key[self.__letters[0]],self.__key[self.__letters[1]] = self.__key[self.__letters[1]],self.__key[self.__letters[0]]


    def undoShuffle(self):
        self.__key[self.__letters[0]],self.__key[self.__letters[1]] = self.__key[self.__letters[1]],self.__key[self.__letters[0]]

    def decipher(self):
        plainText = []
        for letter in self.__cipher:
            plainText.append(self.__key[letter])
        return plainText
