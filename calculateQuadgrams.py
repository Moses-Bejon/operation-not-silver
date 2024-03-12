import json
from numpy import *
from unidecode import unidecode
from math import log2

with open("trainingData") as books:
    lines = books.readlines()

def calculateLetterFrequencies():
    letterFrequencies = zeros(26, dtype=uintc)

    for line in lines:

        # removes accents like è becomes e and makes lower case
        line = unidecode(line).lower()

        for letter in line:
            if letter.isalpha():
                letterFrequencies[ord(letter)-97] += 1

    letterFrequencies.tofile("letterFrequencies.bin")

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
