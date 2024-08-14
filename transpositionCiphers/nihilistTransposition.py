from permutationKey import permutationKey
import random

class nihilistTransposition():

    def __init__(self, cipher):
        self.__cipher = cipher
        self.__cipherLength = len(self.__cipher)

        possibleKeyLengths = []

        for i in range(2, int(self.__cipherLength ** 0.5) + 1):
            if self.__cipherLength % i ** 2 == 0:
                possibleKeyLengths.append(i)

        if not possibleKeyLengths:
            print(
                "This is not a nihilist transposition cipher as the number of characters in the cipher is incompatible")
            return

        self.__key = permutationKey(possibleKeyLengths)
        self.updateKeyLength()

        self.__readingOffRows = True
        self.__readFunction = self.readOffRows

    def shuffle(self):
        self.__key.shuffle()

    def undoShuffle(self):
        self.__key.undoShuffle()

    def shake(self):
        if random.random() > 0.8:
            if self.__readingOffRows:
                self.__readingOffRows = False
                self.__readFunction = self.readOffColumns
            else:
                self.__key.shake()
                self.updateKeyLength()

                self.__readingOffRows = True
                self.__readFunction = self.readOffRows
        else:
            for _ in range(3):
                self.shuffle()

    def updateKeyLength(self):
        self.__length = self.__key.getLength()
        self.__lengthSquared = self.__length ** 2
        self.__numberOfBlocks = round(self.__cipherLength / self.__lengthSquared)

        print(self.__numberOfBlocks)

        self.saveBlocksInColumn()

    def saveBlocksInColumn(self):
        self.__cipherBlocks = []
        for block in range(self.__numberOfBlocks):

            currentBlock = []
            beginBlockAt = block * self.__lengthSquared

            for i in range(self.__length):

                row = []
                beginRowAt = beginBlockAt + i * self.__length

                for j in range(self.__length):
                    row.append(self.__cipher[beginRowAt + j])
                currentBlock.append(row)
            self.__cipherBlocks.append(currentBlock)

    def saveBlocksInRow(self):

        self.__cipherBlocks = [[] for _ in range(self.__numberOfBlocks)]

        gridWidth = self.__length*self.__numberOfBlocks

        for row in range(self.__length):

            beginRowAt = row*gridWidth

            for block in range(self.__numberOfBlocks):

                blockRow = []
                beginBlockAt = beginRowAt+block*self.__length

                for column in range(self.__length):
                    blockRow.append(self.__cipher[beginBlockAt+column])

                self.__cipherBlocks[block].append(blockRow)


    def decipherBlock(self, block, key):

        columnShuffleBlock = [[]] * self.__length

        for i in range(self.__length):
            newRow = []
            for j in key:
                newRow.append(block[i][j])
            columnShuffleBlock[i] = newRow

        rowShuffleBlock = []

        for i in key:
            rowShuffleBlock.append(columnShuffleBlock[i])

        return rowShuffleBlock

    def readOffRows(self, decodedBlock):
        plainText = []

        for row in range(self.__length):
            for character in decodedBlock[row]:
                plainText.append(character)

        return plainText

    def readOffColumns(self, decodedBlock):
        plainText = []

        for column in range(self.__length):
            for row in range(self.__length):
                plainText.append(decodedBlock[row][column])

        return plainText

    def decipher(self):

        plainText = []

        key = self.__key.getKey()

        for block in self.__cipherBlocks:
            plainText += self.__readFunction(self.decipherBlock(block, key))

        return plainText
