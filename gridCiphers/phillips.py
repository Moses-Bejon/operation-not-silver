# To be run in hillClimbWithMargin. Optimal conditions: margin = 0.2*length Chance to shuffle = 0.5

from copy import deepcopy
from polybiusGridEnhancedShuffle import polybiusGridEnhancedShuffle

def intToString(cipher):
    formattedCipher = ""
    for letter in cipher:
        # if letter >= 9:
        #     letter += 1  # adjust to skip 'j'
        formattedCipher += chr(letter + 97)
    return formattedCipher


# print(intToString([8,8,10]))
def stringToInt(cipher):
    formattedCipher = []
    for letter in cipher:
        if letter.lower() == 'j':
            letter = 'i'
        if letter.isalpha():
            formattedCipher.append(ord((letter).lower()) - 97)
    # return [c if c < 9 else c - 1 for c in formattedCipher]
    return formattedCipher


class Phillips():  # also name the file the same way please

    def __init__(self, ciphertext, keyword=None):
        self.__cipher = stringToInt(ciphertext)  # now integers
        self.__key = polybiusGridEnhancedShuffle()
        print("keysquare", self.__key.getGrid())

        self.__keyword = keyword

    def generateKeySquare(self, kw):  # only for decrypting with known keyword/dict attack
        # if length > 18: # too big
        #     return None
        alphabet = [i for i in range(26)]
        alphabet.remove(9)
        keyword = stringToInt(kw)
        keyword += alphabet
        keySquare = []

        for char in keyword:
            if char not in keySquare:
                keySquare.append(char)
                # print(intToString(keySquare))

        # if length >0:
        #     random.shuffle(key[:length])
        # print("generate keysquare", keySquare)
        return keySquare

    def gridTo1d(self,k):
        x = []
        for i in k:
            for j in i:
                x.append(j)

        return x

    '''
    Returns: list of all 8 squares derived from keySquares (included)
    '''
    def generateSquares(self):
        # shift row 1 i.e. first 5 down the line

        squares = [self.gridTo1d(self.__key.getGrid())]
        prevSquare = squares[0]
        for row in range(0, 7):  # swap this row with next row
            row %= 4  # determines which row we're pinned to move
            square = deepcopy(prevSquare)
            starting = (row % 5) * 5
            ending = (row + 1) % 5 * 5
            nextEnding = (row + 2) % 5 * 5
            moving = prevSquare[starting: ending]
            square[starting:ending] = square[ending:nextEnding]
            square[ending:nextEnding] = moving
            squares.append(square)
            prevSquare = square

        return squares

    def shuffle(self):
        self.__key.shuffle()
        # in phillips, flip along L->R has no effect on mapping, and R->L reverses everything - originally K->D would turn into D->K. Not recommended

    def undoShuffle(self):
        self.__key.undoShuffle()

    def decipher(self):
        # decrypt ciphertext in blocks of 5
        plaintext = []
        squares = self.generateSquares()

        for block in range(len(self.__cipher) // 5 + 1):
            for l in range(block * 5, block * 5 + 5, 1):
                if l >= len(self.__cipher):
                    break
                letter = self.__cipher[l]
                square = squares[block % 8]
                row, col = divmod(square.index(letter), 5)
                plainRow, plainCol = (row - 1) % 5, (col - 1) % 5  # going back Northwest
                plaintext.append(square[plainRow * 5 + plainCol])

        return plaintext
