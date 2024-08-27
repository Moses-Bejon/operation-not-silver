from copy import deepcopy
import random
from .nihilist import Nihilist
from .playfair import playfair
from hillClimb import hillClimb

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


class Phillips(playfair): # also name the file the same way please

    def __init__(self,ciphertext, keyword=None):
        super().__init__(ciphertext)
        self.__cipher = stringToInt(ciphertext) # now integers
        # print("ciphertext", self.__cipher)
        # self.__swappedLetters = (-1, -1)
        self.__key = self.generateKey(keyword)
        print("keysquare", self.__key)
        self.__prevKey = None
        # playfair's self.__key represents the keysquare now
        
        self.__keyword = (keyword)

    def generateKey(self, kw=None):
        # exclude (ideally) letter j from alphabet - this is for 5x5 grid
        if kw:
            return self.generateKeySquare(kw)
        alphabet = [i for i in range(26)]
        alphabet.remove(9)
        random.shuffle(alphabet)
        return [alphabet[i:i+5] for i in range(0,25,5)]

        # return alphabet
    
    def generateKeySquare(self, kw): # only for decrypting with known keyword/dict attack
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
    
    def generateSquares(self):
        '''
        Returns: list of all 8 squares derived from keySquares (included)'''
        # shift row 1 i.e. first 5 down the line
        def gridTo1d(k):
            x = []
            for i in k:
                for j in i:
                    x.append(j)

            return x
        squares = [gridTo1d(self.__key)]
        prevSquare = squares[0]
        for row in range(0,7): # swap this row with next row
            row %= 4 # determines which row we're pinned to move
            square = deepcopy(prevSquare)
            starting = (row%5) * 5
            ending = (row+1)%5 *5
            # if ending == 0:
            #     ending = 25
            nextEnding = (row+2) %5 *5
            # if nextEnding == 0:
            #     nextEnding = 25
            moving = prevSquare[starting: ending]
            square[starting:ending] = square[ending:nextEnding]
            square[ending:nextEnding] = moving
            squares.append(square)
            prevSquare = square
            # print(row, intToString(prevSquare))

        return squares
        

    # def shuffle(self):
    #     # code to randomly shuffle the key (the shuffle should be the smallest shuffle possible such that the plain text
    #     # deciphered is as similar to the previous as possible)
    #     # try shift column with small probability
    #     l1, l2 = random.sample(self.__key, 2)
    #     self.__key = Nihilist.swap_letters(self.__key, l1, l2)
    #     self.__swappedLetters = (l1, l2)
    #     return self.__key
        

    # this is an optional function feel free to remove it
    # if the hill climb thinks it's reached a local maximum, it will call this function, to attempt to break out
    # if you have removed it the cipher will simply be shuffled ten times instead
    def shake(self):
        choice = random.random()
        if choice <= 0.15:
            self.swapRows(self.__key)
        elif choice <= 0.3:
            self.swapColumns(self.__key)
        else:
            for _ in range(5):
                self.shuffle(self.__key)
    def shuffle(self, k=None):
        self.__prevKey = deepcopy(self.__key)
        choice = random.random()
        if choice <=0.8:
            self.swapElements(self.__key)
            # print(self.__key)
        elif choice <=0.95:
            if random.random() >= 0.5:
                self.swapRows(self.__key)
            else:
                self.swapColumns(self.__key)
        # # in phillips, flip along L->R has no effect on mapping, and R->L reverses everything - originally K->D would turn into D->K. Not recommended
        
        # # elif choice <= 0.15:
        #     # self.flipDiagonal() 
        # elif choice <= 0.99:
        #     # flip the square around the diagonal that runs from upper left to lower right
        #     self.flipVertical()
        #     print("AAAAH")
        # else:
        #     self.flipHorizontal() # basically everything changes apart from the columns they're in... not too sure, basically a row rearrangement
        return self.__key
    def undoShuffle(self):
        # only needs to undo one previous shuffle. This function will not be called twice in a row, only ever with a
        # # shuffle() in between
        self.__key = deepcopy(self.__prevKey)
        # a, b = random.randint(0,4), random.randint(0,4)
        # self.__key[5*a:5*a + 5], self.__key[5*b:5*b+5] = self.__key[5*b:5*b+5], self.__key[5*a:5*a + 5]
        # self.__key = Nihilist.swap_letters(self.__key, self.__swappedLetters[0], self.__swappedLetters[1])


    def decipher(self, something=None):
        # decrypt ciphertext in blocks of 5
        plaintext = []
        squares = self.generateSquares()
        
        for block in range(len(self.__cipher)//5+1):
            for l in range(block*5, block*5+5, 1):
                if l >= len(self.__cipher):
                    break
                letter = self.__cipher[l]
                square = squares[block % 8]
                row, col = divmod(square.index(letter), 5)
                plainRow, plainCol = (row-1)%5, (col-1)%5 # going back Northwest
                plaintext.append(square[plainRow*5 + plainCol])
        # print("Inttostring of ps",intToString(plaintext))
        return((plaintext))

