import random

# 2021 mission 7A

class polybiusSquare(): # also name the file the same way please

    def __init__(self,cipher):
        self.__cipher = cipher # the cipherText
        self.__key = ""
        self.__grid = ["abcde", "fghik", "lmnop", "qrstu", "vwxyz"]


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
        # code to get plainText from self.__cipher using self.__key (or whatever keys you're using)
        # def generateGrid(key):
        #     key.replace('i','j')
        #     s = set(key)
        #     unduplicatedKey = ''
        #     for c in key:
        #         if c not in unduplicatedKey else for c in key

        #     alphabet = set('abcdefghiklmnopqrstuvwxyz')
        #     rest = alphabet - set(key) # take out used letters
        #     rest = key + rest # concactenate 
        #     # this 1d 2d array reminds me of dastan
        #     self.__grid = [rest[:5], rest[5:10], rest[10:15], rest[15:20], rest[20:]]

        indices = {}
        for i in range(len(self.__grid)):
            for j in range(len(self.__grid)):
                letter = self.__grid[i][j]
                indices[str(i+1) + str(j+1)] = letter
        
        plainText = ''
        for k in range(0, len(self.__cipher), 2):
            c = self.__cipher[k:k+2]
            plainText += indices[c]


            
            
        return plainText
    
with open("ciphertext.txt", 'r') as f:
    cipher = polybiusSquare(f.read().replace(' ', ''))
    print(cipher.decipher())