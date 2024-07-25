import random

import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import from the parent directory
from monoalphabeticSubstitutionCiphers.monoAlphabeticSubstitution import monoAlphabeticSubstitution
from formatCipher import stringToInt
# not sure if this importing works for everyone
# 2021 mission 7A, 8B

class polybiusSquare(monoAlphabeticSubstitution): # also name the file the same way please
    
    def __init__(self,cipher):
        self.__grid = ["abcde", "fghik", "lmnop", "qrstu", "vwxyz"]
        super().__init__(self.polybiusify(cipher))


    def polybiusify(self, cipher):
        # switch the numbers into basic letters
        indices = {}
        for i in range(len(self.__grid)):
            for j in range(len(self.__grid)):
                letter = self.__grid[i][j]
                indices[str(i+1) + str(j+1)] = letter
        
        letterified = ''
        for k in range(0, len(cipher), 2):
            c = cipher[k:k+2]
            letterified += indices[c]
        # print(letterified)
        return stringToInt(letterified)
    
