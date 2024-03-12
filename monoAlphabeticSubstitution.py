import random

class monoAlphabeticSubstitution():
  
    def __init__(self,cipher):
        self.__cipher = cipher
        self.__key = {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f', 'g': 'g', 'h': 'h', 'i': 'i', 'j': 'j', 'k': 'k', 'l': 'l', 'm': 'm', 'n': 'n', 'o': 'o', 'p': 'p', 'q': 'q', 'r': 'r', 's': 's', 't': 't', 'u': 'u', 'v': 'v', 'w': 'w', 'x': 'x', 'y': 'y', 'z': 'z'}

    def shuffle(self):
        self.__letters = random.sample("abcdefghijklmnopqrstuvwxyz",k=2)
        self.__key[self.__letters[0]],self.__key[self.__letters[1]] = self.__key[self.__letters[1]],self.__key[self.__letters[0]]


    def undoShuffle(self):
        self.__key[self.__letters[0]],self.__key[self.__letters[1]] = self.__key[self.__letters[1]],self.__key[self.__letters[0]]

    def decipher(self):
        plainText = ""
        for letter in self.__cipher:
            plainText += self.__key[letter]
        return plainText
