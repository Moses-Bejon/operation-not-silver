import json
from numpy import *

# uses the angle between the two vectors of ideal frequencies and actual frequencies (the bigger the less similar)
# also this seems to be pretty useful as it's very expensive to calculate and not very effective
with open("letterFrequenciesSorted.json","r") as file:
    idealLetterFrequenciesSorted = array(json.load(file),dtype=uintc)
def evaluateLetterFrequenciesSubstituted(plainText):
    letterFrequencies = zeros(26,dtype=uintc)
    for letter in plainText:
        letterFrequencies[letter]+=1
    letterFrequencies = sorted(letterFrequencies)
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
