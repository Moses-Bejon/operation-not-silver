# to be run in hill climb with shake threshold of 5000

import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import from the parent directory
from monoalphabeticSubstitutionCiphers.monoAlphabeticSubstitution import monoAlphabeticSubstitution
from polybiusGrid import polybiusGrid

def formatPolybius(cipher, usingCharacters):
    formattedCipherText = []

    for character in cipher:

        # yes, this is an extremely inefficient approach, but realistically this is only running once
        if character in usingCharacters:
            formattedCipherText.append(usingCharacters.index(character))

    return formattedCipherText

class polybiusSquare(monoAlphabeticSubstitution):  # also name the file the same way please

    def __init__(self, cipher, usingCharacters = ["0","1","2","3","4"]):
        formatted = formatPolybius(cipher,usingCharacters)
        print(formatted)
        grid = polybiusGrid()

        monoAlphabeticText = []

        for k in range(0, len(formatted), 2):
            monoAlphabeticText.append(grid.getCharacterAtCoordinates(formatted[k+1],formatted[k]))

        super().__init__(monoAlphabeticText)
