import random

class fourSquare():
    def __init__(self,cipher):
        self.__cipher = cipher

        self.__grid1 = {'a': (0, 0), 'b': (0, 1), 'c': (0, 2), 'd': (0, 3), 'e': (0, 4), 'f': (1, 0), 'g': (1, 1), 'h': (1, 2),
             'i': (1, 3), 'k': (1, 4), 'l': (2, 0), 'm': (2, 1), 'n': (2, 2), 'o': (2, 3), 'p': (2, 4), 'q': (3, 0),
             'r': (3, 1), 'v': (3, 2), 't': (3, 3), 'u': (3, 4), 's': (4, 0), 'w': (4, 1), 'x': (4, 2), 'y': (4, 3),
             'z': (4, 4)}
        self.__grid2 = {'a': (0, 0), 'i': (0, 1), 'c': (0, 2), 'd': (0, 3), 'e': (0, 4), 'f': (1, 0), 'g': (1, 1), 'h': (1, 2),
             'b': (1, 3), 'k': (1, 4), 'l': (2, 0), 'm': (2, 1), 'n': (2, 2), 'o': (2, 3), 'p': (2, 4), 'q': (3, 0),
             'r': (3, 1), 's': (3, 2), 't': (3, 3), 'u': (3, 4), 'v': (4, 0), 'w': (4, 1), 'x': (4, 2), 'y': (4, 3),
             'z': (4, 4)}

        # the polybius square
        self.__defaultGrid = ("abcde", "fghik", "lmnop", "qrstu", "vwxyz")


    def shuffle(self):

        if random.random()>0.5:
            self.__currentGrid = self.__grid1
        else:
            self.__currentGrid = self.__grid2

        self.__letters = random.sample("abcdefghiklmnopqrstuvwxyz",k=2)

        # swaps two random letters in chosen grid
        self.__currentGrid[self.__letters[0]], self.__currentGrid[self.__letters[1]] = self.__currentGrid[self.__letters[1]], self.__currentGrid[self.__letters[0]]

    def undoShuffle(self):
        self.__currentGrid[self.__letters[0]], self.__currentGrid[self.__letters[1]] = self.__currentGrid[self.__letters[1]], self.__currentGrid[self.__letters[0]]

    def decipher(self):
        # to be filled up
        plainText = ""

        # for every pair of letters in the cipher text (since the cipher encodes bigrams)
        for i in range(int(len(self.__cipher) / 2)):
            # stores the characters in letter1 and letter2
            letter1 = self.__cipher[i * 2]
            letter2 = self.__cipher[i * 2 + 1]

            # computes what letters the cipher text letters map to and adds it to the plain text
            plainText += self.__defaultGrid[self.__grid1[letter1][0]][self.__grid2[letter2][1]] +\
                         self.__defaultGrid[self.__grid2[letter2][0]][self.__grid1[letter1][1]]

        return plainText
