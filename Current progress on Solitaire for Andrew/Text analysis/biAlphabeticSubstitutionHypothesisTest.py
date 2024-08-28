import random
import math
from scipy.stats import binom
from formatCipher import *
import json

class bigram:
    def __init__(self):
        self.__frequency = 1  # if we were instantiated, there must be 1 of us so far
        self.__possibleMappings = set()

    def addFrequency(self):
        self.__frequency += 1

    def getFrequency(self):
        return self.__frequency

    def getMappings(self):
        return self.__possibleMappings

    def addMapping(self,mapping):
        self.__possibleMappings.add(mapping)

    def removeMapping(self,mapping):
        self.__possibleMappings.remove(mapping)


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

            for bigramHash,proportion in self.__idealBigrams:

                if bigramData.getFrequency() < numberOfBigrams*proportion:
                    probability = binom.cdf(bigramData.getFrequency(),numberOfBigrams,proportion)
                else:
                    probability = 1-binom.cdf(bigramData.getFrequency()-1,numberOfBigrams,proportion)

                if probability > 0.001:
                    bigramData.addMapping(bigramHash)

        contained = 0
        totalLength = 0
        for bigramData,data in bigrams.items():
            print(intToString(bigramData),len(data.getMappings()))
            totalLength += len(data.getMappings())
            if bigramData[0]*26+bigramData[1] in data.getMappings():
                print("contained")
                contained += 1
            else:
                print("missing")

        print(f"{contained} were contained out of {len(bigrams)}. The total number of bigrams used was {totalLength}")

cipher = stringToInt("""

“Ah!” He tried the roll top tentatively. “Locked. But perhaps one of
Mrs. Inglethorp’s keys would open it.” He tried several, twisting and
turning them with a practiced hand, and finally uttering an ejaculation
of satisfaction. “_Voilà!_ It is not the key, but it will open it at a
pinch.” He slid back the roll top, and ran a rapid eye over the neatly
filed papers. To my surprise, he did not examine them, merely remarking
approvingly as he relocked the desk: “Decidedly, he is a man of method,
this Mr. Inglethorp!”

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
