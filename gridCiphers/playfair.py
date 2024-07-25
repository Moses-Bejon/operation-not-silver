import random

class playfair(): # also name the file the same way please

    def __init__(self,cipher):
        self.__cipher = cipher # the cipherText
        self.__key = "any valid key or group of keys, you can split this up into multiple variables if you need to"

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
        return plainText
