# these functions are all quite inefficient but that should be fine since they all run in reasonable time and only
# need to be run once to generate files and never again

from unidecode import unidecode
from math import log2
import json

with open("trainingData") as books:
    lines = books.readlines()

def calculateLetterFrequencies():
    letterFrequencies = []

    for letter in range(26):
        letterFrequencies.append([letter,0])

    count = 0
    for line in lines:

        # removes accents like è becomes e and makes lower case
        line = unidecode(line).lower()

        for letter in line:
            if letter.isalpha():
                letterFrequencies[ord(letter)-97][1] += 1
                count += 1

    letterFrequencyValues = []
    for pair in letterFrequencies:
        letterFrequencyValues.append(pair[1])
    with open("letterFrequenciesUnsorted.json","w") as file:
        json.dump(letterFrequencyValues, file)

    letterFrequencies = sorted(letterFrequencies,key=lambda x: x[1],reverse=True)

    letterFrequencyValues = []
    letterFrequencyLetters = []
    for pair in letterFrequencies:
        letterFrequencyLetters.append(pair[0])
        letterFrequencyValues.append(pair[1])
    with open("lettersRanked.json","w") as file:
        json.dump(letterFrequencyLetters,file)
    with open("letterFrequenciesSorted.json","w") as file:
        json.dump(letterFrequencyValues,file)

    normalisedLetterFrequencies = []
    for letter in letterFrequencyValues:
        normalisedLetterFrequencies.append(letter/count)
    with open("letterFrequenciesSortedNormalised.json","w") as file:
        json.dump(normalisedLetterFrequencies,file)

def calculateAlphanumericQuadgramFrequencies():
    quadgramFrequencies = {}

    # beginning us with the most common quadgram "that"
    window = [ord("t") - 97, ord("h") - 97, ord("a") - 97, ord("t") - 97]
    total = 0

    for line in lines:

        # removes accents like è becomes e and makes lower case
        line = unidecode(line).lower()

        for letter in line:
            if letter.isalpha():

                total += 1

                try:
                    # lists are not hashable because they are immutable
                    quadgramFrequencies[tuple(window)] += 1
                except:
                    quadgramFrequencies[tuple(window)] = 1

                window.pop(0)
                window.append(ord(letter) - 97)

            elif letter.isdigit():

                total += 1

                try:
                    # lists are not hashable because they are immutable
                    quadgramFrequencies[tuple(window)] += 1
                except:
                    quadgramFrequencies[tuple(window)] = 1

                window.pop(0)
                window.append(ord(letter) - 48+26)

    hashMap = [-25] * (36 ** 4)

    for quadgram, frequency in quadgramFrequencies.items():
        hashMap[quadgram[0] * 36 ** 3 + quadgram[1] * 36 ** 2 + quadgram[2] * 36 + quadgram[3]] = log2(
            frequency / total)

    with open("alphanumeric quadgram proportions.json", "w") as file:
        json.dump(hashMap, file)

    hashMap = [0] * (36 ** 4)

    for quadgram, frequency in quadgramFrequencies.items():
        hashMap[quadgram[0] * 36 ** 3 + quadgram[1] * 36 ** 2 + quadgram[2] * 36 + quadgram[3]] = frequency / total

    with open("alphanumeric quadgram proportions unlogged.json", "w") as file:
        json.dump(hashMap, file)

def calculateQuadgramFrequencies():
    quadgramFrequencies = {}

    # beginning us with the most common quadgram "that"
    window = [ord("t")-97,ord("h")-97,ord("a")-97,ord("t")-97]
    total = 0

    for line in lines:

        # removes accents like è becomes e and makes lower case
        line = unidecode(line).lower()

        for letter in line:
            if letter.isalpha():

                total += 1

                try:
                    # lists are not hashable because they are immutable
                    quadgramFrequencies[tuple(window)] += 1
                except:
                    quadgramFrequencies[tuple(window)] = 1

                window.pop(0)
                window.append(ord(letter)-97)

    hashMap = [-25] * (26 ** 4)

    for quadgram,frequency in quadgramFrequencies.items():
        hashMap[quadgram[0]*26**3+quadgram[1]*26**2+quadgram[2]*26+quadgram[3]] = log2(frequency/total)

    with open("quadgram proportions.json","w") as file:
        json.dump(hashMap,file)

    hashMap = [0]*(26**4)

    for quadgram,frequency in quadgramFrequencies.items():
        hashMap[quadgram[0]*26**3+quadgram[1]*26**2+quadgram[2]*26+quadgram[3]] = frequency/total

    with open("quadgram proportions unlogged.json","w") as file:
        json.dump(hashMap,file)

def calculateTrigramFrequencies():
    trigramFrequencies = {}
    window = [ord("t") - 97, ord("h") - 97, ord("e") - 97]
    total = 0

    for line in lines:
        line = unidecode(line).lower()

        for letter in line:
            if letter.isalpha():

                total += 1

                try:
                    trigramFrequencies[tuple(window)] += 1
                except:
                    trigramFrequencies[tuple(window)] = 1

                window.pop(0)
                window.append(ord(letter) - 97)

    hashMap = [-25] * (26 ** 3)

    for trigram, frequency in trigramFrequencies.items():
        hashMap[trigram[0] * 26 ** 2 + trigram[1] * 26 + trigram[2]] = log2(frequency / total)

    with open("trigram proportions.json", "w") as file:
        json.dump(hashMap, file)

def calculateBigramFrequencies():
    bigramFrequencies = {}
    window = [ord("t")-97,ord("h")-97]
    total = 0

    for line in lines:

        # removes accents like è becomes e and makes lower case
        line = unidecode(line).lower()

        for letter in line:
            if letter.isalpha():

                total += 1

                try:
                    bigramFrequencies[tuple(window)] += 1
                except:
                    bigramFrequencies[tuple(window)] = 1

                window.pop(0)
                window.append(ord(letter) - 97)

    print(total)

    bigramFrequenciesOrdered = sorted(bigramFrequencies.keys(),key=lambda x: bigramFrequencies[x],reverse=True)

    with open("bigrams ranked.json","w") as file:
        json.dump(bigramFrequenciesOrdered,file)

    hashMap = [-25]*(26**2)

    for quadgram,frequency in bigramFrequencies.items():
        hashMap[quadgram[0]*26+quadgram[1]] = log2(frequency/total)

    with open("bigram proportions.json","w") as file:
        json.dump(hashMap,file)

    hashMap = [0]*(26**2)

    for quadgram,frequency in bigramFrequencies.items():
        hashMap[quadgram[0]*26+quadgram[1]] = frequency/total

    print(hashMap)

    for i,hash in enumerate(hashMap):
        if hash == 0:
            print(i)

    with open("bigram proportions unlogged.json","w") as file:
        json.dump(hashMap,file)


calculateAlphanumericQuadgramFrequencies()
