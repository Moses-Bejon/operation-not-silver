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
        self.cipherText = cipherText
        self.key = self.generateKey()

    def generateKey(self):
        # exclude (ideally) letter j from alphabet - this is for 5x5 grid
        alphabet = [i for i in range(25)]
        random.shuffle(alphabet)
        return alphabet

    def decipher(self):
        plainText = []
        for i in range(0, len(self.cipherText),2):
            a = self.cipherText[i]
            b = self.cipherText[i+1]
            plainText.extend(self.decodePair(a,b))
        return plainText

    def decodePair(self, a, b):
        rowA, colA = divmod(self.key.index(a), 5)
        rowB, colB = divmod(self.key.index(b), 5)

        if rowA == rowB:
            return [(rowA * 5 + (colA - 1) % 5), (rowB * 5 + (colB - 1) % 5)]
        elif colA == colB:
            return [((rowA-1)%5 * 5 + colA), ((rowB-1)%5 * 5 + colB)]
        else:
            return [(rowA * 5 + colB), (rowB * 5 + colA)]


    def shuffle(self):
        choice = random.randint(1, 6)
        if choice == 1:
            self.swapElements()
        elif choice == 2:
            self.swapRows()
        elif choice == 3:
            self.swapColumns()
        elif choice == 4:
            self.flipDiagonal()
        elif choice == 5:
            # flip the square around the diagonal that runs from upper left to lower right
            self.flipVertical()
        elif choice == 6:
            self.flipHorizontal()

    def swapElements(self):
        a,b = random.sample(range(25),2)
        self.key[a], self.key[b] = self.key[b], self.key[a]

    def swapRows(self):
            rowA, rowB = random.sample(range(25), 2)
            self.key[rowA * 5:rowA * 5 + 5], self.key[rowB * 5:rowB * 5 + 5] = self.key[rowB * 5:rowB * 5 + 5], self.key[rowA * 5:rowA * 5 + 5]

    def swapColumns(self):
        colA, colB = random.sample(range(5), 2)
        for i in range(5):
            self.key[i * 5 + colA], self.key[i * 5 + colB] = self.key[i * 5 + colB], self.key[i * 5 + colA]

    def flipDiagonal(self):
        self.key = [self.key[i%5 * 5+i //5] for i in range(25)]

    def flipVertical(self):
        for i in range(5):
            self.key[i*5:(i+1) * 5] = self.key[i*5:(i+1) * 5][::-1]

    def flipHorizontal(self):
        self.key = self.key[::-1]

def evaluate(plaintext):
    bigramScore = evaluateBigramFrequencies(plaintext)
    quadgramScore = evaluateQuadgramFrequencies(plaintext)
    letterFreq, _ = getLetterFrequencies(plaintext)
    iocScore = getIOC(letterFreq, len(plaintext))

    totalScore = bigramScore + quadgramScore + 2 * iocScore
    return totalScore


cipherText = "UDSDAEEPVFHPKNNMPILPBMNGDOOGHPGDVFHIVQRSURBETIREAFHPAVKFREHRRMFANFPUDMRAAUPIAGPEXFTGRUODWRBNFNDOTGPWQGDMNLQVWEUWHGLDFSAUNOQPUALZSDZDGUFABEZDRBDFDVVQRSGMBEIZTDFNOPPLPUUVRBAUGTVEHRARFKDRBEODUDVEUCAWRBPRDSNEBXRSLTPWQGRAFAKGLPUWHGLZBFREIEREZLRETZWGYNLPDUFPECPZZDMUGUUTICGUIARAODOQGDUGIZGHUALZMUBVZDDMZDRBGUFAEFBRDMARDFOPBRPRNLOMSDSRXNOREBRADMGKANMHKIDZUMOAPLOAAFUNRZARSIGHUSMGZDRDEPUWBEIFREOPLSFNBWAUMPTLMGNLRZARSIPIAUXGZDPR"

cipherText = stringToInt(cipherText)
playfair = playfair(cipherText)

key, decryption = simulatedAnnealing(
    playfair.key,
    playfair.shuffle,
    lambda dec: evaluate(playfair.decipher()),
    playfair.decipher
)

print(f'Best key: {key}')
print(f'Best decrypt: {intToString(decryption)}')



