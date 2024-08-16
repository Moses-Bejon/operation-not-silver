import random

from permutationKey import permutationKey

class cadenus():

    def __init__(self,cipher,columnLength = 25):
        self.__cipher = cipher
        self.__columnLength = columnLength

        self.__length = len(self.__cipher)
        self.__totalRows = self.__length/self.__columnLength

        if self.__totalRows%1 != 0:
            print("The column length and cipher length are not a valid pair")
            return

        self.__totalRows = round(self.__length/self.__columnLength)

        possibleKeyLengths = []

        # yes, this is quite an inefficient way to do this
        # I don't care because it's clean and this step is only done once
        # it will never make up a significant proportion of total computation time of the algorithm
        for i in range(2,self.__totalRows):
            if self.__totalRows%i == 0:
                possibleKeyLengths.append(i)

        if not possibleKeyLengths:
            print("The column length and cipher length are not a valid pair")
            return

        self.__permutationKey = permutationKey(possibleKeyLengths)
        self.updatePermutationKeyLength()

    def shuffle(self):

        # could potentially optimise by using the same random number if necessary
        if random.random() > 0.5:
            self.__previousShuffleMode = 0
            self.__permutationKey.shuffle()
        else:
            if random.random() > 0.5:
                self.__previousShuffleMode = 1
                self.__index = int(random.random()*self.__keyLength)
                self.__value = self.__shiftKey[self.__index]
                self.__shiftKey[self.__index] = int(random.random()*(self.__columnLength+1))
            else:
                self.__previousShuffleMode = 2
                self.__value = int(random.random()*self.__columnLength+1)
                for i in range(self.__keyLength):
                    self.__shiftKey[i] += self.__value

    def undoShuffle(self):
        match self.__previousShuffleMode:
            case 0:
                self.__permutationKey.undoShuffle()
            case 1:
                self.__shiftKey[self.__index] = self.__value
            case 2:
                for i in range(self.__keyLength):
                    self.__shiftKey[i] -= self.__value

    def updatePermutationKeyLength(self):
        self.__keyLength = len(self.__permutationKey.getKey())
        self.__shiftKey = [0] * self.__keyLength

        self.__numberOfBlocks = round(self.__totalRows / self.__keyLength)
        self.__cipherBlocks = []

        blockLength = self.__keyLength * self.__columnLength
        for block in range(self.__numberOfBlocks):

            currentBlock = []
            beginBlockAt = block * blockLength

            for i in range(self.__columnLength):

                row = []
                beginRowAt = beginBlockAt + i * self.__keyLength

                for j in range(self.__keyLength):
                    row.append(self.__cipher[beginRowAt + j])
                currentBlock.append(row)
            self.__cipherBlocks.append(currentBlock)

    def shake(self):
        if random.random() > 0.95:
            self.__permutationKey.shake()
            self.updatePermutationKeyLength()
        else:
            for _ in range(3):
                self.shuffle()

    def decipherBlock(self,block,permutationKey):
        permutedBlock = []

        for row in block:
            newRow = []
            for position in permutationKey:
                newRow.append(row[position])
            permutedBlock.append(newRow)

        shiftedBlock = []

        for i in range(self.__columnLength):

            newRow = []

            for j in range(self.__keyLength):

                newRow.append(permutedBlock[(i+self.__shiftKey[j])%self.__columnLength][j])

            shiftedBlock.append(newRow)

        return shiftedBlock

    def readOffRows(self, decodedBlock):
        plainText = []

        for row in range(self.__columnLength):
            for character in decodedBlock[row]:
                plainText.append(character)

        return plainText

    def readOffColumns(self, decodedBlock):
        plainText = []

        for column in range(self.__keyLength):
            for row in range(self.__columnLength):
                plainText.append(decodedBlock[row][column])

        return plainText

    def decipher(self):

        plainText = []

        permutationKey = self.__permutationKey.getKey()

        for block in self.__cipherBlocks:
            plainText += self.readOffRows(self.decipherBlock(block,permutationKey))

        return plainText
