from linguisticData.evaluate import getIOC, getLetterFrequencies, evaluateBigramFrequencies, evaluateQuadgramFrequencies
from formatCipher import stringToInt


class trithemius():  # also name the file the same way please

    def __init__(self, cipher):
        cipher = cipher.replace("\n", "").upper()
        cipher = cipher.replace(" ", "").upper()
        self.__cipher = cipher  # the cipherText
        self.listOfKeys = []
        # do any computation you need to do beforehand here
        for s in range(26):
            for pmod in ['p+s', 'p-s', 's-p']:
                self.listOfKeys.append([pmod,s])


    def plainTexts(self):
        for keys in self.listOfKeys:
            # calculate plain text
            plain = ''
            for char in self.__cipher:
                p = ord(char) - 65
                if keys[0] == 'p+s':
                    p = (p - keys[1]) % 26
                elif keys[0] == 'p-s':
                    p = (p + keys[1]) % 26
                elif keys[0] == 's-p':
                    p = (keys[1] - (p+1)) % 26
                p = chr(p + 65)
                keys[1] += 1
                plain += p
            yield stringToInt(plain)
