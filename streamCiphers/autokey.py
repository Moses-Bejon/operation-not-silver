import random
import json
import math
from evaluate import getIOC, getEntropy, getLetterFrequencies, normaliseLetterFrequencies, evaluateBigramFrequencies, evaluateQuadgramFrequencies
from formatCipher import stringToInt, intToString

class polyalphabeticSubstitution:
    def __init__(self, cipher):
        self.cipher = cipher
        self.period, self.frequencies = self.getPeriod()
        self.key = self.getKey()

    def getPeriod(self):
        # lowest possible score
        maxScore = -1
        maxPeriod = 1

        # trying out different periods to see which fits best (up to cipher length)
        for n in range(2, int(len(self.cipher) ** 0.5)+1):

            # these are the different slices of the cipher text
            slices = [[] for _ in range(n)]

            # populating slices based on period
            for place in range(len(self.cipher)):
                slices[place % n].append(self.cipher[place])

            # checking fitness of slices
            totalScore = 0

            sliceLetterFrequencies = []
            for slice in slices:
                letterFrequencies, total = getLetterFrequencies(slice)
                totalScore += getIOC(letterFrequencies, total) * getEntropy(
                    normaliseLetterFrequencies(letterFrequencies, total))
                sliceLetterFrequencies.append(letterFrequencies)

            averageScore = totalScore / n

            if averageScore > maxScore:
                maxScore = averageScore
                maxPeriod = n

        # empty frequency list to be populated later
        return maxPeriod, []

    def getKey(self):
        key = []
        with open("lettersRanked.json", "r") as file:
            idealRank = json.load(file)

            # formulates key based on letter frequencies to get a good starting guess
        for frequency in self.frequencies:

            letterFrequencies = sorted(enumerate(frequency), key=lambda x: x[1], reverse=True)

            alphabet = {}
            for i in range(26):
                alphabet[letterFrequencies[i][0]] = idealRank[i]
            key.append(alphabet)
        return key


class autokey(polyalphabeticSubstitution):
    def __init__(self, cipher):
        super().__init__(cipher)
        self.bestKey = None
        self.bestDecryption = None
        self.bestScore = float('-inf')

    def decipher(self, cipherText, key):
        plainText = []
        keyIndex = 0

        # calculate shift from key and reverse shift to decrypt char
        for char in cipherText:
            shift = key[keyIndex % len(key)]
            decryptedChar = (char-shift) % 26
            plainText.append(decryptedChar)
            keyIndex += 1
            # update the key with plainText char
            key.append(decryptedChar)
        return plainText

    # evaluate the fitness of the decrypted plainText
    def evaluateDecryption(self, plainText):
        bigramScore = evaluateBigramFrequencies(plainText)
        quadgramScore = evaluateQuadgramFrequencies(plainText)
        letterFreq, _ = getLetterFrequencies(plainText)
        iocScore = getIOC(letterFreq, len(plainText))

        totalScore = bigramScore + quadgramScore + 2 * iocScore
        return totalScore

    # brute force the best key-length, can change the maxKeyLength if needed
    def bruteForceAutokey(self, maxKeyLength=20):
        bestKeyLength = 1
        bestScore = float('-inf')

        # try key lengths from 1 to maxKeyLength, test 500 random keys for each key length
        for keyLength in range(1, maxKeyLength+1):
            for _ in range(500):
                key = [random.randint(0,25) for _ in range(keyLength)]
                decryptedText = self.decipher(self.cipher, key)
                score = self.evaluateDecryption(decryptedText)

                if score > bestScore:
                    bestScore = score
                    bestKeyLength = keyLength

        return bestKeyLength

    # optimise decryption process
    def simulatedAnnealing(self, keyLength, initialTemp=100.0, coolingRate=0.95, maxIter=1000):
        currentKey = [random.randint(0, 25) for _ in range(keyLength)]  
        bestKey = currentKey[:]  
        bestDecryption = None  
        bestScore = float('-inf')  

        temperature = initialTemp  

        for iteration in range(maxIter):
            candidateKey = currentKey[:]
            pos = random.randint(0, keyLength - 1)
            candidateKey[pos] = random.randint(0, 25)

            # Decrypt with candidate key and evaluate decryption
            decryptedText = self.decipher(self.cipher, candidateKey.copy())
            candidateScore = self.evaluateDecryption(decryptedText)

            # accept or reject new score
            deltaScore = candidateScore - bestScore

            if deltaScore > 0 or random.uniform(0, 1) < math.exp(deltaScore / temperature):
                currentKey = candidateKey[:]
                if candidateScore > bestScore:
                    bestScore = candidateScore
                    bestKey = candidateKey[:]
                    bestDecryption = decryptedText

            # reduce temp
            temperature *= coolingRate

            if iteration % 100 == 0:
                print(f"Iteration: {iteration}, Best Score: {bestScore}, Best Key: {bestKey}")

        self.bestKey = bestKey
        self.bestDecryption = bestDecryption
        self.bestScore = bestScore

        return bestKey, intToString(bestDecryption)


# cipherText = "PLEKLARLUSGSOSAOWAWLQWGBLSBLUFPAVSGNAPDLIPLHTGBCARDAQEIVVJGVQHVMQOVGKIPHISELWDWHWFFTWJFRHIPYIGNGOSGFZABUKNIKFQAIFXBFVRTXKMPBPUPPRVSCZEVQAEUXZBXNHWXZHBOAVHWNKALQDCGEJWOFRMSRMNFRPVNMGJOIMAKMYAMNHXMOEKTOKWVSISRXUQWJITEJPWOSQTGSHDSKNSXMPSDCASLOZNLKFAZTNHJJZEQXIYPFYOGEOVGRYLENSSPDNSPKHTWJMNHAMCYMOSLHIRORSMOKSMHBUDMVQGKMAGNLQAQQAZOSDEEGPPPZGDMSQEPTPILMWMVVVTVVFVQZSVK"
# cipherText = stringToInt(cipherText)
# autokeyCipher = autokey(cipherText)

# keyLength = autokeyCipher.bruteForceAutokey(maxKeyLength=20)

# bestKey, decryptedText = autokeyCipher.simulatedAnnealing(keyLength)
# print("Best Key:", bestKey)
# print("Decrypted Text:", decryptedText)
