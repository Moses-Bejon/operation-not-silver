from numpy import *
import json

# uses the angle between the two vectors of ideal frequencies and actual frequencies (the bigger the less similar)
# also this seems to be pretty useful as it's very expensive to calculate and not very effective
idealLetterFrequencies = fromfile("Text analysis/letterFrequencies.bin",dtype=uintc)
def evaluateLetterFrequencies(plainText):
    letterFrequencies = zeros(26,dtype=uintc)
    for letter in plainText:
        letterFrequencies[ord(letter)-97]+=1
    return dot(letterFrequencies,idealLetterFrequencies)/(linalg.norm(letterFrequencies)*linalg.norm(idealLetterFrequencies))

# a much better, and computationally cheaper, approach. Logged quadgram frequencies (the more negative, the less similar)
with open("Text analysis/quadgram proportions.json","r") as file:
    idealQuadgramFrequencies = json.load(file)
floor = -25 # this is the value when something appears 0 times in our ideal text (very negative because not very similar)
# if something appears once it's about -21
def evaluateQuadgramFrequencies(plainText):
    window = plainText[:4]
    fitness = 0
    for letter in plainText[4:]:
        try:
            fitness += idealQuadgramFrequencies[window]
        except:
            fitness += floor
        window = window[1:] + letter
    return fitness
