from polybiusGrid import polybiusGrid

class doublePlayfairKnownKey:

    def __init__(self, keyword1, keyword2, fill1=None, fill2 = None):
        self.grid1 = polybiusGrid()
        self.grid2 = polybiusGrid()
        alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'

        self.fillGrid(self.grid1, keyword1, alphabet, fill1)
        self.fillGrid(self.grid2, keyword2, alphabet, fill2)

    def fillGrid(self, grid, keyword, alphabet, fill):
        remainingLetters = [char for char in alphabet if char not in keyword]
        characters = keyword + ''.join(remainingLetters)

        if fill == 'horizontal':
            grid.fillHorizontally(characters)
        elif fill == 'vertical':
            grid.fillVertically(characters)
        elif fill == 'spiralCW':
            grid.fillSpiralCW(characters)
        elif fill == 'spiralCCW':
            grid.fillSpiralCCW(characters)
        else:
            print('ERROR')

    def decodePair(self, a, b):
        posA = self.grid1.getCoordinatesOfCharacter(a)
        posB = self.grid2.getCoordinatesOfCharacter(b)

        colA, rowA = posA
        colB, rowB = posB

        # handles wraparounds
        if rowA == rowB:
            # same row= shift columns left
            newA = self.grid1.getCharacterAtCoordinates((colA - 1 + 5) % 5, rowA)
            newB = self.grid2.getCharacterAtCoordinates((colB - 1 + 5) % 5, rowB)
        elif colA == colB:
            # same column= shift rows up
            newA = self.grid1.getCharacterAtCoordinates(colA, (rowA - 1 + 5) % 5)
            newB = self.grid2.getCharacterAtCoordinates(colB, (rowB - 1 + 5) % 5)
        else:
            # rectangle swap= swap columns, keep rows
            newA = self.grid1.getCharacterAtCoordinates(colB, rowA)
            newB = self.grid2.getCharacterAtCoordinates(colA, rowB)

        return newA, newB

    def decipher(self, cipherText, period):
        plainText = [''] * len(cipherText)

        # deal with adjacent pairs first
        for i in range(0, len(cipherText), 2):
            a = cipherText[i]
            b = cipherText[i + 1]

            newA, newB = self.decodePair(a, b)
            finalA, finalB = self.decodePair(newA, newB)

            # split text based on period
            plainText[i // 2] = finalA
            plainText[(i // 2) + period] = finalB

        return ''.join(plainText)

    def testPeriods(self, cipherText, maxPeriod=None):
        for period in range(1, maxPeriod +1):
            plainText = self.decipher(cipherText, period)
            print (f'Period: {period}: {plainText}')


cipherText = 'TWFAATNIOYRAXMTAMZAOMRIVASEAPRIGAAFQAK'

keyword1 = 'POLYBIUS'
keyword2 = 'KEYWORD'

test = doublePlayfairKnownKey(keyword1, keyword2, fill1="horizontal", fill2="vertical")
plainText = test.decipher(cipherText, 7)
test.testPeriods(cipherText, 10)
