import json
from numpy import *
from unidecode import unidecode
from math import log2

with open("trainingData") as books:
    lines = books.readlines()

def calculateLetterFrequencies():
    letterFrequencies = [['a', 0], ['b', 0], ['c', 0], ['d', 0], ['e', 0], ['f', 0], ['g', 0], ['h', 0], ['i', 0], ['j', 0], ['k', 0], ['l', 0], ['m', 0], ['n', 0], ['o', 0], ['p', 0], ['q', 0], ['r', 0], ['s', 0], ['t', 0], ['u', 0], ['v', 0], ['w', 0], ['x', 0], ['y', 0], ['z', 0]]

    for line in lines:

        # removes accents like è becomes e and makes lower case
        line = unidecode(line).lower()

        for letter in line:
            if letter.isalpha():
                letterFrequencies[ord(letter)-97][1] += 1

    letterFrequencyValues = []
    for pair in letterFrequencies:
        letterFrequencyValues.append(pair[1])
    with open("letterFrequenciesUnsorted.json","w") as file:
        json.dump(letterFrequencyValues, file)

    letterFrequencies = sorted(letterFrequencies,key=lambda x: x[1])

    letterFrequencyValues = []
    letterFrequencyLetters = []
    for pair in letterFrequencies:
        letterFrequencyLetters.append(pair[0])
        letterFrequencyValues.append(pair[1])
    with open("lettersRanked.json","w") as file:
        json.dump(letterFrequencyLetters,file)
    with open("letterFrequenciesSorted.json","w") as file:
        json.dump(letterFrequencyValues,file)

def calculateQuadgramFrequencies():
    quadgramFrequencies = {}
    window = "that"
    total = 0

    for line in lines:

        # removes accents like è becomes e and makes lower case
        line = unidecode(line).lower()

        for letter in line:
            if letter.isalpha():

                total += 1

                try:
                    quadgramFrequencies[window] += 1
                except:
                    quadgramFrequencies[window] = 1

                window = window[1:]+letter

    for quadgram,frequency in quadgramFrequencies.items():
        quadgramFrequencies[quadgram] = log2(frequency/total)

    with open("quadgram proportions.json","w") as file:
        json.dump(quadgramFrequencies,file)

def calculateBigramFrequencies():
    bigramFrequencies = {}
    window = "th"
    total = 0

    for line in lines:

        # removes accents like è becomes e and makes lower case
        line = unidecode(line).lower()

        for letter in line:
            if letter.isalpha():

                total += 1

                try:
                    bigramFrequencies[window] += 1
                except:
                    bigramFrequencies[window] = 1

                window = window[1:]+letter

    bigramFrequenciesOrdered = sorted(bigramFrequencies.keys(),key=lambda x: bigramFrequencies[x],reverse=True)

    with open("bigrams ranked.json","w") as file:
        json.dump(bigramFrequenciesOrdered,file)

    for quadgram,frequency in bigramFrequencies.items():
        bigramFrequencies[quadgram] = log2(frequency/total)

    with open("bigram proportions.json","w") as file:
        json.dump(bigramFrequencies,file)
