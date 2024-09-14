from polybiusGrid import polybiusGrid
# MAKE SURE THE KEYWORDS DO NOT CONTAIN ANY REPEATED LETTERS

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
        # Find the positions of the letters in their respective grids
        posA = self.grid1.getCoordinatesOfCharacter(a)
        posB = self.grid2.getCoordinatesOfCharacter(b)

        colA, rowA = posA
        colB, rowB = posB

        # print(f'decode pair: {a} ({posA}) and {b} ({posB})')

        # handles wraparounds
        if rowA == rowB:
            # same row = shift columns right
            newA = self.grid1.getCharacterAtCoordinates((colA + 1) % 5, rowA)
            newB = self.grid2.getCharacterAtCoordinates((colB + 1) % 5, rowB)

        else:
            # rectangle swap = swap col, keep rows
            newA = self.grid1.getCharacterAtCoordinates(colA, rowB)
            newB = self.grid2.getCharacterAtCoordinates(colB, rowA)

        return newA, newB

    def decipher(self, cipherText, period):
        top = []
        bottom = []

        # deal with adjacent pairs first
        for i in range(0, len(cipherText), 2):
            a = cipherText[i]
            b = cipherText[i + 1]

            # print(a, b)

            newA, newB = self.decodePair(a, b)
            finalA, finalB = self.decodePair(newB, newA)
            finalB, finalA = finalA, finalB

            # print(f'final stuff: {finalA},{finalB}')

            # split text based on period

            top.append(finalA)
            bottom.append(finalB)

            combineTop = [top[i:i+period] for i in range(0, len(top), period)]
            combineBottom = [bottom[i:i+period] for i in range(0, len(bottom), period)]

            plainText = []
            for i in range(max(len(combineTop), len(combineBottom))):
                if i < len(combineTop):
                    plainText.append(combineTop[i])
                if i < len(combineBottom):
                    plainText.append(combineBottom[i])

            li2 = [ y for x in plainText for y in x]
        return ''.join(map(str,li2))

    def testPeriods(self, cipherText, maxPeriod=None):
        for period in range(1, maxPeriod +1):
            plainText = self.decipher(cipherText, period)
            print (f'Period: {period}: {plainText}')


# cipherText = 'DTQFQAKMGIMEAEQHRVZDATAANIFOHUTMFIBXTTRFQMFIFIHDGURWTIPSSBIKTEDFLAKVANUSOHIMQBVASSACONLDVEALAEHNGIGUELPEESGPCBFNFIRFSIKVITNGQMDXQBXISIAHIASHAIGKLBECCQAFMMGUTTFDNKEIDBSIHUCDNCOMKKGIMMGXTTTBRCBCRBDPBDSLZZLDQEDPBMSMRAFFELMESSBDOCEEREPELBIIPGQBTFTTKBTBXSKKGUQHFNUDQRDYLU'
#
# keyword1 = 'GRIDON'
# keyword2 = 'FOTBAL'
#
# test = doublePlayfairKnownKey(keyword2, keyword1, fill1="horizontal", fill2="horizontal")
# plainText = test.decipher(cipherText, 6)
# # test.testPeriods(cipherText, 10)
# print(plainText)
