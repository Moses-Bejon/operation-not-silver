import random
from unidecode import unidecode
from evaluate import getIOC, getLetterFrequencies, evaluateBigramFrequencies, evaluateQuadgramFrequencies
from simulatedAnnealing import simulatedAnnealing

# need to swap j for i
def stringToInt(cipher):
    formattedCipher = []
    for letter in cipher:
        if letter.lower() == 'j':
            letter = 'i'
        if letter.isalpha():
            formattedCipher.append(ord(unidecode(letter).lower()) - 97)
    return [c if c < 9 else c - 1 for c in formattedCipher]

def intToString(cipher):
    formattedCipher = ""
    for letter in cipher:
        if letter >= 9:
            letter += 1  # adjust to skip 'j'
        formattedCipher += chr(letter + 97)
    return formattedCipher

class playfair:
    def __init__(self, cipherText):
        self.__cipherText = cipherText
        self.__key = self.generateKey()

    def generateKey(self):
        # exclude (ideally) letter j from alphabet - this is for 5x5 grid
        alphabet = [i for i in range(25)]
        random.shuffle(alphabet)
        return [alphabet[i:i+5] for i in range(0,25,5)]

    def decipher(self, key):
        plainText = []
        for i in range(0, len(self.__cipherText), 2):
            a = self.__cipherText[i]
            b = self.__cipherText[i + 1]
            plainText.extend(self.decodePair(a, b, key))
        return plainText

    def decodePair(self, a, b, key):
        posA = [(ix, iy) for ix, row in enumerate(key) for iy, i in enumerate(row) if i == a][0]
        posB = [(ix, iy) for ix, row in enumerate(key) for iy, i in enumerate(row) if i == b][0]

        rowA, colA = posA
        rowB, colB = posB

        if rowA == rowB:
            # same row= shift columns left
            new_a = key[rowA][(colA - 1) % 5]
            new_b = key[rowB][(colB - 1) % 5]
        elif colA == colB:
            # same col= shift rows up
            new_a = key[(rowA - 1) % 5][colA]
            new_b = key[(rowB - 1) % 5][colB]
        else:
            # swap columns but keep rows
            new_a = key[rowA][colB]
            new_b = key[rowB][colA]

        return [new_a, new_b]

    def shuffle(self, key):
        key = [row[:] for row in key]
        choice = random.randint(1, 6)
        if choice == 1:
            self.swapElements(key)
        elif choice == 2:
            self.swapRows(key)
        elif choice == 3:
            self.swapColumns(key)
        elif choice == 4:
            self.flipDiagonal(key)
        elif choice == 5:
            self.flipVertical(key)
        elif choice == 6:
            self.flipHorizontal(key)
        return key
        # Debug print
        # self.printKey()

    def swapElements(self, key):
        a, b = random.sample(range(25), 2)
        rowA, colA = divmod(a, 5)
        rowB, colB = divmod(b, 5)
        key[rowA][colA], key[rowB][colB] = key[rowB][colB], key[rowA][colA]

    def swapRows(self, key):
        rowA, rowB = random.sample(range(5), 2)
        key[rowA], key[rowB] = key[rowB], key[rowA]

    def swapColumns(self, key):
        colA, colB = random.sample(range(5), 2)
        for i in range(5):
            key[i][colA], key[i][colB] = key[i][colB], key[i][colA]

    def flipDiagonal(self, key):
        key[:] = [[key[j][i] for j in range(5)] for i in range(5)]

    def flipVertical(self, key):
        key.reverse()

    def flipHorizontal(self, key):
        for i in range(5):
            key[i] = key[i][::-1]

    def printKey(self):
        print("current Key:")
        if self.__key:
            for row in self.__key:
                print(row)

    def evaluateDecryption(self, plainText):
        bigramScore = evaluateBigramFrequencies(plainText)
        quadgramScore = evaluateQuadgramFrequencies(plainText)
        letterFreq, _ = getLetterFrequencies(plainText)
        iocScore = getIOC(letterFreq, len(plainText))

        totalScore = bigramScore + quadgramScore + 2 * iocScore
        return totalScore

    def generateCandidateKey(self, currentKey):
        candidateKey = self.shuffle(currentKey)
        # debug print statement
        # print(f'Shuffled key: {candidateKey}')
        return candidateKey

    def decrypt(self, key):
        plainText = self.decipher(key)
        # print(f'Decrypted text: {intToString(plainText)}')
        return plainText


cipherText = "MDSOASOGTGKCDRBZEQVSKYMHFVIBDSKYMHCOROCEGODGABUICQMRORAOEAIHPEVFHPDMQCXCNDPUMRKBBPASZKGQPLABKENPNBVIQCASYQWBGZGUAEKYKBSHIQBUFSCPVLEQOEGUPBBNEQRFQYQCKSZGDCGUQSSIDCKGOGKRXZEQDKFVSAUCOCLNMRRCHWCMOBVFPDNBLVXCPEDRMHFVPDFVOVRCEAHRFSRLXCZMGQUQBXKGGSOBPUNPMDSHQBUIFNSGDUDUDCOWGSRFYTCYMRDSLTRDBXARZRQGKDQITVPLFVOIASDPQWQRDRXCPEGECRVFEDPLCDSDMCBAIQDQPLCOBNVBOZURBYXCNURQBXNQWSEKQUTCIQAELTFICZEQSHOGHWGENLTMTCPLEKBAUNAEOW"

cipherText = stringToInt(cipherText)
playfairCipher = playfair(cipherText)


initialKey = playfairCipher.generateKey()
bestKey, bestDecryption = simulatedAnnealing(
    initialKey=initialKey,
    generateCandidateKey=playfairCipher.generateCandidateKey,
    evaluateFitness=lambda dec: playfairCipher.evaluateDecryption(dec),
    decrypt=lambda key: playfairCipher.decrypt(key),
    maxIter=20000,
    coolingRate=0.999
)

print(f'Best key: {bestKey}')
print(f'Best decryption: {intToString(bestDecryption)}')



