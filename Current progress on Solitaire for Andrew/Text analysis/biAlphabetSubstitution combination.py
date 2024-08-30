import random
import math
from scipy.stats import binom
from formatCipher import *
import json

class bigram:
    def __init__(self):
        self.__frequency = 1  # if we were instantiated, there must be 1 of us so far
        self.__possibleMappings = {}

    def addFrequency(self):
        self.__frequency += 1

    def getFrequency(self):
        return self.__frequency

    def getMappings(self):
        return self.__possibleMappings

    def addMapping(self,mapping,probability):
        self.__possibleMappings[mapping] = probability

    def removeMapping(self,mapping):
        del self.__possibleMappings[mapping]


class biAlphabeticSubstitution():
    def __init__(self, cipher):

        numberOfBigrams = int(len(cipher) / 2)
        bigrams = {}

        for i in range(numberOfBigrams):

            try:
                bigrams[(cipher[2 * i], cipher[2 * i + 1])].addFrequency()
            except:
                bigrams[(cipher[2 * i], cipher[2 * i + 1])] = bigram()

        with open("bigram proportions unlogged.json", "r") as file:
            self.__idealBigrams = list(enumerate(json.load(file)))

        for bigramData in bigrams.values():

            totalProbability = 0
            probabilityArray = []

            for bigramHash,proportion in self.__idealBigrams:

                probability = binom.pmf(bigramData.getFrequency(),numberOfBigrams,proportion)

                totalProbability += probability

                probabilityArray.append((bigramHash,probability))

            actualTotalProbability = 0

            sortedArray = sorted(probabilityArray,reverse=True,key=lambda x:x[1])

            mostProbableBigramProbability = sortedArray[0][1]/totalProbability

            for bigramHash,probability in sortedArray:

                actualProbability = probability/totalProbability

                actualTotalProbability += actualProbability


                if actualTotalProbability > 0.9995 or mostProbableBigramProbability-actualProbability>0.3:
                    break

                bigramData.addMapping(bigramHash, actualProbability)

        contained = 0
        totalLength = 0

        output = {}

        for bigramData, data in bigrams.items():
            output[intToString(bigramData)] = data.getMappings()
            print(intToString(bigramData), len(data.getMappings()))
            totalLength += len(data.getMappings())
            if bigramData[0] * 26 + bigramData[1] in data.getMappings():
                print("contained")
                contained += 1
            else:
                print("missing")

        print(f"{contained} were contained out of {len(bigrams)}. The total number of bigrams used was {totalLength}")

        with open("output.json","w") as outputFile:
            json.dump(output,outputFile)

cipher = stringToInt("""

""")
cipherType = biAlphabeticSubstitution(cipher)

'''
def bruteClimb(cipher, evaluate):
    maxPlainText = cipher.decipher()
    maxScore = evaluate(maxPlainText)
    actualMaxScore = maxScore

    count = 0

    # records how long we've been not climbing up the hill
    withoutClimbing = 0

    while True:
        count += 1
        withoutClimbing += 1

        iterationMax = maxScore
        bestChoice = None
        for _ in range(500):
            cipher.shuffle()

            plainText = cipher.decipher()
            score = evaluate(plainText)

            if score > iterationMax:
                iterationMax = score
                bestChoice = cipher.getShuffle()

            cipher.undoShuffle()

        if bestChoice != None:
            cipher.controlledShuffle(bestChoice)
            maxScore = iterationMax
            if iterationMax > actualMaxScore:
                print(cipher.decipher())
                print(count)
                print(iterationMax)
                actualMaxScore = iterationMax
                maxScore = iterationMax
        else:
            cipher.shuffle()
            maxScore = evaluate(cipher.decipher())


from evaluate import evaluateQuadgramFrequencies
'''
