import json
from numpy import *
from math import log

def getIOC(letterFrequencies,total):
    return sum(letter*(letter-1) for letter in letterFrequencies)/(total*(total-1))

# letter frequencies must be sorted and normalised
with open("letterFrequenciesSortedNormalised.json","r") as file:
    idealLetterFrequenciesSortedNormalised = json.load(file)
def getTwist(letterFrequencies):
    twist = 0
    for i in range(13):
        twist += idealLetterFrequenciesSortedNormalised[i + 13]-idealLetterFrequenciesSortedNormalised[i]+(letterFrequencies[i]-letterFrequencies[i + 13])
    return twist

# letter frequencies must be normalised
def getEntropy(letterFrequencies):
    entropy = 0
    for frequency in letterFrequencies:
        try:
            entropy -= frequency*log(frequency,26)
        except:
            entropy += frequency*1.5
    return entropy

def getLetterFrequencies(plainText):
    letterFrequencies = [0]*26
    total = 0
    for letter in plainText:
        letterFrequencies[letter] += 1
        total += 1
    return (letterFrequencies,total)

def normaliseLetterFrequencies(letterFrequencies,total):
    normalisedLetterFrequencies = []
    for letter in letterFrequencies:
        normalisedLetterFrequencies.append(letter/total)
    return normalisedLetterFrequencies

# letter frequencies must be sorted
with open("letterFrequenciesSorted.json") as file:
    idealLetterFrequenciesSorted = json.load(file)
def getVectorEvaluationSubstituted(letterFrequencies):
    return dot(letterFrequencies,idealLetterFrequenciesSorted)/(linalg.norm(letterFrequencies)*linalg.norm(idealLetterFrequenciesSorted))

with open("letterFrequenciesUnsorted.json","r") as file:
    idealLetterFrequenciesUnsorted = array(json.load(file),dtype=uintc)
def evaluateLetterFrequenciesUnsubstituted(plainText):
    letterFrequencies = zeros(26, dtype=uintc)
    for letter in plainText:
        letterFrequencies[letter] += 1
    return dot(letterFrequencies, idealLetterFrequenciesUnsorted) / (
                linalg.norm(letterFrequencies) * linalg.norm(idealLetterFrequenciesUnsorted))

# a much better, and computationally cheaper, approach. Logged quadgram frequencies (the more negative, the less similar)
with open("quadgram proportions.json","r") as file:
    idealQuadgramFrequencies = json.load(file)
def evaluateQuadgramFrequencies(plainText):

    currentHash = plainText[0]*17576+plainText[1]*676+plainText[2]*26+plainText[3]

    fitness = 0
    for i in range(len(plainText)-4):
        first = plainText[i] * 17576
        last = plainText[i+4]
        fitness += idealQuadgramFrequencies[currentHash]
        currentHash = 26*(currentHash-first)+last
    return fitness

with open("bigram proportions.json","r") as file:
    idealBigramFrequencies = json.load(file)
def evaluateBigramFrequencies(plainText):

    fitness = 0
    for i in range(len(plainText)-1):
        fitness += idealBigramFrequencies[plainText[i]*26+plainText[i+1]]
    return fitness
