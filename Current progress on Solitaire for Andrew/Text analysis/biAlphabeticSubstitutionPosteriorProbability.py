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

            totalProbability = 0
            probabilityArray = []

            for bigramHash,proportion in self.__idealBigrams:

                probability = binom.pmf(bigramData.getFrequency(),numberOfBigrams,proportion)

                totalProbability += probability

                probabilityArray.append((bigramHash,probability))

            actualTotalProbability = 0
            for bigramHash,probability in sorted(probabilityArray,reverse=True,key=lambda x:x[1]):
                bigramData.addMapping(bigramHash)
                actualTotalProbability += probability/totalProbability
                if actualTotalProbability > 0.999:
                    break

        contained = 0
        totalLength = 0
        for bigramData, data in bigrams.items():
            print(intToString(bigramData), len(data.getMappings()))
            totalLength += len(data.getMappings())
            if bigramData[0] * 26 + bigramData[1] in data.getMappings():
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

A “man of method” was, in Poirot’s estimation, the highest praise that
could be bestowed on any individual.

I felt that my friend was not what he had been as he rambled on
disconnectedly:

“There were no stamps in his desk, but there might have been, eh, _mon
ami?_ There might have been? Yes”—his eyes wandered round the
room—“this boudoir has nothing more to tell us. It did not yield much.
Only this.”
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
