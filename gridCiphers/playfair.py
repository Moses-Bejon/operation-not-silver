from copy import deepcopy
import random
from unidecode import unidecode
from evaluate import evaluateQuadgramFrequencies

# need to swap j for i
def stringToInt(cipher):
    formattedCipher = []
    for letter in cipher:
        if letter.lower() == 'j':
            letter = 'i'
        if letter.isalpha():
            formattedCipher.append(ord(unidecode(letter).lower()) - 97)
    return [c if c < 9 else c - 1 for c in formattedCipher]

def intToString(cipher):
    formattedCipher = ""
    for letter in cipher:
        if letter >= 9:
            letter += 1  # adjust to skip 'j'
        formattedCipher += chr(letter + 97)
    return formattedCipher

class playfair:
    def __init__(self, cipherText):
        self.__cipherText = cipherText
        self.__key = self.generateKey()

    def generateKey(self):
        # exclude (ideally) letter j from alphabet - this is for 5x5 grid
        alphabet = [i for i in range(25)]
        random.shuffle(alphabet)
        return [alphabet[i:i+5] for i in range(0,25,5)]

    def decipher(self):

        plainText = []
        for i in range(0, len(self.__cipherText), 2):
            a = self.__cipherText[i]
            b = self.__cipherText[i + 1]
            plainText.extend(self.decodePair(a, b))
        # print(plainText)
        return plainText

    def decodePair(self, a, b):
        posA = [(ix, iy) for ix, row in enumerate(self.__key) for iy, i in enumerate(row) if i == a][0]
        posB = [(ix, iy) for ix, row in enumerate(self.__key) for iy, i in enumerate(row) if i == b][0]

        rowA, colA = posA
        rowB, colB = posB

        if rowA == rowB:
            # same row= shift columns left
            newA = self.__key[rowA][(colA - 1) % 5]
            newB = self.__key[rowB][(colB - 1) % 5]
        elif colA == colB:
            # same col= shift rows up
            newA = self.__key[(rowA - 1) % 5][colA]
            newB = self.__key[(rowB - 1) % 5][colB]
        else:
            # swap columns but keep rows
            newA = self.__key[rowA][colB]
            newB = self.__key[rowB][colA]

        return [newA, newB]

    def shuffle(self):
        self.__previousKey = deepcopy(self.__key)

        self.__key = [row[:] for row in self.__key]
        choice = random.randint(1, 100)
        if choice <= 90:
            self.swapElements()
        elif choice <= 92:
            self.swapRows()
        elif choice <= 94:
            self.swapColumns()
        elif choice <= 96:
            self.flipDiagonal()
        elif choice <= 98:
            self.flipVertical()
        else:
            self.flipHorizontal()

        # Debug print
        # self.printKey()

    def undoShuffle(self):
        self.__key = self.__previousKey

    def swapElements(self):
        a, b = random.sample(range(25), 2)
        rowA, colA = divmod(a, 5)
        rowB, colB = divmod(b, 5)
        self.__key[rowA][colA], self.__key[rowB][colB] = self.__key[rowB][colB], self.__key[rowA][colA]

    def swapRows(self):
        rowA, rowB = random.sample(range(5), 2)
        self.__key[rowA], self.__key[rowB] = self.__key[rowB], self.__key[rowA]

    def swapColumns(self):
        colA, colB = random.sample(range(5), 2)
        for i in range(5):
            self.__key[i][colA], self.__key[i][colB] = self.__key[i][colB], self.__key[i][colA]

    def flipDiagonal(self):
        self.__key[:] = [[self.__key[j][i] for j in range(5)] for i in range(5)]

    def flipVertical(self):
        self.__key.reverse()

    def flipHorizontal(self):
        for i in range(5):
            self.__key[i] = self.__key[i][::-1]

    def printKey(self):
        print("current Key:")
        if self.__key:
            for row in self.__key:
                print(row)

    def evaluateDecryption(self, plainText):
        newPlainText = []
        for i in plainText:
            if i > 8:
                newPlainText.append(i+1)
            else:
                newPlainText.append(i)
        quadgramScore = evaluateQuadgramFrequencies(newPlainText)
        return quadgramScore
