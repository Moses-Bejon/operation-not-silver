import random
from unidecode import unidecode
from evaluate import getIOC, getLetterFrequencies, evaluateBigramFrequencies, evaluateQuadgramFrequencies
from simulatedAnnealing import simulatedAnnealing
from copy import deepcopy

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

def createDigraphs(cipher):
    digraphs = []
    i = 0
    while i < len(cipher):
        a = cipher[i]
        if i + 1 < len(cipher):
            b = cipher[i + 1]
            if a == b:
                digraphs.append([a, 23])  # 'x' corresponds to 23
                i += 1
            else:
                digraphs.append([a, b])
                i += 2
        else:
            digraphs.append([a, 23])  # 'x' corresponds to 23
            i += 1
    return digraphs

class playfair:
    def __init__(self, cipherText, key=None):
        self.__cipherText = cipherText
        if key is None:
            self.__key = self.generateKey()
            self.__keySquare = self.__key
        else:
            if isinstance(key, str):
                self.__keySquare = self.createSquare(key)
            else:
                self.__keySquare = key

    def createSquare(self, key):
        keySquare = []
        usedNumbers = set()

        for letter in key:
            num = ord(letter) - 97
            if num == 9:  # Skip 'j'
                continue
            num = num if num < 9 else num - 1  # Adjust for 'j'
            if num not in usedNumbers:
                keySquare.append(num)
                usedNumbers.add(num)

        for num in range(25):
            if num not in usedNumbers:
                keySquare.append(num)
                usedNumbers.add(num)

        # Return the 5x5 key square
        return [keySquare[i * 5:(i + 1) * 5] for i in range(5)]

    def findPosition(self, num):
        for row in range(5):
            for col in range(5):
                if self.__keySquare[row][col] == num:
                    return row, col

    def generateKey(self):
        # exclude (ideally) letter j from alphabet - this is for 5x5 grid
        alphabet = [i for i in range(25)]
        random.shuffle(alphabet)
        return [alphabet[i:i+5] for i in range(0,25,5)]

    # def decipher(self, key):
    #     plainText = []
    #     for i in range(0, len(self.__cipherText), 2):
    #         a = self.__cipherText[i]
    #         b = self.__cipherText[i + 1]
    #         decodedPair = self.decodePair(a, b, key)
    #         plainText.extend(decodedPair)
    #
    #     return plainText

    def decipher(self):
        digraphs = createDigraphs(self.__cipherText)
        plainText = []
        for pair in digraphs:
            plainText.extend(self.decodePair(pair))

        return plainText

    def decodePair(self, digraph):
        # convert 9 to 8
        a,b = digraph

        rowA, colA = self.findPosition(a)
        rowB, colB = self.findPosition(b)

        if rowA == rowB:
            # Same row: shift columns left
            return [self.__keySquare[rowA][(colA - 1) % 5], self.__keySquare[rowB][(colB - 1) % 5]]
        elif colA == colB:
            # Same column: shift rows up
            return [self.__keySquare[(rowA - 1) % 5][colA], self.__keySquare[(rowB - 1) % 5][colB]]
        else:
            # Rectangle: swap columns
            return [self.__keySquare[rowA][colB], self.__keySquare[rowB][colA]]

    def shuffle(self, key):
        key = deepcopy(key)
        choice = random.randint(1, 100)
        if choice <= 90:
            self.swapElements(key)
        elif choice <= 92:
            self.swapRows(key)
        elif choice <= 94:
            self.swapColumns(key)
        elif choice <= 96:
            self.flipDiagonal(key)
        elif choice <= 98:
            self.flipVertical(key)
        else:
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

    def convert(self, text):
        # any number after 8 should be incremented by one by evaluator
        # print(f'text: {intToString(text)}')
        return [8 if c == 9 else c for c in text]
        # return [c + 1 if c > 8 else c for c in text]

    def evaluateDecryption(self, plainText):
        convertedText = self.convert(plainText)
        # print(f'converted text: {intToString(convertedText)}')
        quadgramScore = evaluateQuadgramFrequencies(convertedText)
        return quadgramScore

    def generateCandidateKey(self, currentKey):
        candidateKey = self.shuffle(currentKey)
        # debug print statement
        # print(f'Shuffled key: {candidateKey}')
        return candidateKey

    # def decrypt(self, key):
    #     plainText = self.decipher(key)
    #     # print(f'Decrypted text: {intToString(plainText)}')
    #     return plainText



cipherText = "MDSOASOGTGKCDRBZEQVSKYMHFVIBDSKYMHCOROCEGODGABUICQMRORAOEAIHPEVFHPDMQCXCNDPUMRKBBPASZKGQPLABKENPNBVIQCASYQWBGZGUAEKYKBSHIQBUFSCPVLEQOEGUPBBNEQRFQYQCKSZGDCGUQSSIDCKGOGKRXZEQDKFVSAUCOCLNMRRCHWCMOBVFPDNBLVXCPEDRMHFVPDFVOVRCEAHRFSRLXCZMGQUQBXKGGSOBPUNPMDSHQBUIFNSGDUDUDCOWGSRFYTCYMRDSLTRDBXARZRQGKDQITVPLFVOIASDPQWQRDRXCPEGECRVFEDPLCDSDMCBAIQDQPLCOBNVBOZURBYXCNURQBXNQWSEKQUTCIQAELTFICZEQSHOGHWGENLTMTCPLEKBAUNAEOW"

cipherText = stringToInt(cipherText)

# # known key
# key = "GROCEISABDFHKLMNPQTUVWXYZ"
# key = key.lower()
# 
# playfairCipher = playfair(cipherText, key)
# 
# print(f'integer cipher: {cipherText}')
# decrypt = playfairCipher.decipher()
# decrypt = intToString(decrypt)
# decrypt = decrypt.replace('x', '')
# print(f'Decryption: {decrypt}')


# unknown key 
playfairCipher = playfair(cipherText)
initialKey = playfairCipher.generateKey()
bestKey, bestDecryption = simulatedAnnealing(
    initialKey=initialKey,
    generateCandidateKey=playfairCipher.generateCandidateKey,
    evaluateFitness=lambda dec: playfairCipher.evaluateDecryption(dec),
    decrypt=lambda key: playfairCipher.decipher(),
    maxIter=10000,
    coolingRate=0.999,
    initialTemp=100.0
)

print(f'Best key: {bestKey}')
print(f'Best decryption: {intToString(bestDecryption)}')


