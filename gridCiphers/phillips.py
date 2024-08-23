from copy import deepcopy
import random
from nihilist import Nihilist
# from playfair import intToString - unidecode wouldn't work on my laptop

def intToString(cipher):
    formattedCipher = ""
    for letter in cipher:
        if letter >= 9:
            letter += 1  # adjust to skip 'j'
        formattedCipher += chr(letter + 97)
    return formattedCipher

def stringToInt(cipher):
    formattedCipher = []
    for letter in cipher:
        if letter.lower() == 'j':
            letter = 'i'
        if letter.isalpha():
            formattedCipher.append(ord((letter).lower()) - 97)
    return [c if c < 9 else c - 1 for c in formattedCipher]


class Phillips(): # also name the file the same way please

    def __init__(self,cipher, keyword=None):
        self.__cipher = cipher # the cipherText
        # we don't need valid nums
        self.__keyword = keyword
        self.__keySquare = self.generateKeySquare(keyword)
        self.__swappedLetters = (-1, -1)

    
    def generateKeySquare(self, keyw):
        # if length > 18: # too big
        #     return None
        alphabet = list(range(25))
        keyword = stringToInt(keyw)
        keyword += alphabet
        keySquare = []
        
        for char in keyword:
            if char not in keySquare:
                keySquare.append(char) 
        print(intToString(keySquare))
        # print(keySquare)
        
        # if length >0:
        #     random.shuffle(key[:length])
        return keySquare
    
    def generateSquares(self):
        '''
        Returns: list of all 8 squares derived from keySquares (included)'''
        # shift row 1 i.e. first 5 down the line
        squares = [self.__keySquare]
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
            print(row, intToString(prevSquare))

        return squares
        

    def shuffle(self):
        # code to randomly shuffle the key (the shuffle should be the smallest shuffle possible such that the plain text
        # deciphered is as similar to the previous as possible)
        
        l1, l2 = random.sample(self.__keySquare, 2)
        self.__keySquare = Nihilist.swap_letters(self.__keySquare, l1, l2)
        self.__swappedLetters = (l1, l2)
        

    # this is an optional function feel free to remove it
    # if the hill climb thinks it's reached a local maximum, it will call this function, to attempt to break out
    # if you have removed it the cipher will simply be shuffled ten times instead
    # def shake(self):
    #     pass

    def undoShuffle(self):
        # only needs to undo one previous shuffle. This function will not be called twice in a row, only ever with a
        # shuffle() in between
        self.__keySquare = Nihilist.swap_letters(self.__keySquare, self.__swappedLetters[0], self.__swappedLetters[1])


    def decipher(self):
        # decrypt ciphertext in blocks of 5
        plaintext = []
        squares = self.generateSquares(self.__keySquare)
        
        for block in range(len(self.__cipher)//5+1):
            for l in range(block*5, block*5+5, 1):
                if l >= len(self.__cipher):
                    break
                letter = self.__cipher[l]
                square = squares[block % 8]
                row, col = divmod(square.index(letter), 5)
                plainRow, plainCol = (row-1)%5, (col-1)%5 # going back Northwest
                plaintext.append(square[plainRow*5 + plainCol])
        return(intToString(plaintext))


if __name__ == "__main__":
    cipherString = '''UBSSOOWGUHWHTWFUVHVYDIVLSPGFOWPGFWSNKHAXSAQWAUWUIFKNGU
HQLRQYVGWOIAWGLFGWPFSIYUWNFMQYSHUYNFGIONVYRGYVSIFQNKUW
SFGWSFUYHUIFCMSASQVUQLNGXIGRCUEASGUQWVMIFUIFGWAKWVFQVU
BSGFRYKHGIBNIBUVXPAIYSIVUCZHWGKZBANRGFIFUMWEIYXUNOGWHR
WUZYAUSIAUIHGFMQSIBAUYKYMV
'''
    cipherText = stringToInt(cipherString)
    print(cipherString.lower().replace(' ', '') == intToString(cipherText))
    phillips = Phillips(cipherText)
    print(phillips.decipher())

