from numpy import *
import json

with open("quadgram proportions.json","r") as file:
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