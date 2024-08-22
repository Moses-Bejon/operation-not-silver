from copy import deepcopy
import random
from playfair import stringToInt, intToString
class Phillips(): # also name the file the same way please

    def __init__(self,cipher):
        self.__cipher = cipher # the cipherText
        
        self.__key = self.generateKey("SONGBIRD")
        self.__squares = self.generateSquares()

    
    def generateKey(self, key):
        # if length > 18: # too big
        #     return None
        alphabet = list(range(25))
        keyword = stringToInt(key)
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
        # shift row 1 i.e. first 5 down the line
        squares = [self.__key]
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
        pass

    # this is an optional function feel free to remove it
    # if the hill climb thinks it's reached a local maximum, it will call this function, to attempt to break out
    # if you have removed it the cipher will simply be shuffled ten times instead
    def shake(self):
        pass

    def undoShuffle(self):
        # only needs to undo one previous shuffle. This function will not be called twice in a row, only ever with a
        # shuffle() in between
        pass


    def decipher(self):
        # decrypt ciphertext in blocks of 5
        plaintext = []
        for block in range(len(self.__cipher)//5+1):
            for l in range(block*5, block*5+5, 1):
                if l >= len(self.__cipher):
                    break
                letter = self.__cipher[l]
                square = self.__squares[block % 8]
                row, col = divmod(square.index(letter), 5)
                plainRow, plainCol = (row-1)%5, (col-1)%5 # going back Northwest
                plaintext.append(square[plainRow*5 + plainCol])
        return(intToString(plaintext))


if __name__ == "__main__":
    cipherString = '''ZTPPL NMCBR FLTUO BWBTP RYVFH WBUKK PMWYB VWWC'''
    cipherText = stringToInt(cipherString)
    print(cipherString.lower().replace(' ', '') == intToString(cipherText))
    phillips = Phillips(cipherText)
    print(phillips.decipher())

