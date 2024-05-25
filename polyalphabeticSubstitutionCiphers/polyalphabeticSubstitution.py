import random
import json

from evaluate import getIOC,getEntropy,getLetterFrequencies,normaliseLetterFrequencies

def getPeriod(cipher):

    # lowest possible score
    maxScore = -1

    # trying out different periods to see which fits best
    for n in range(2,int(len(cipher)**0.5)):

        # these are the different slices of the cipher text
        slices = [[] for _ in range(n)]

        # populating slices
        for place in range(len(cipher)):
            slices[place%n].append(cipher[place])

        # checking fitness of slices
        totalScore = 0

        sliceLetterFrequencies = []
        for slice in slices:
            letterFrequencies, total = getLetterFrequencies(slice)
            totalScore += getIOC(letterFrequencies,total)*getEntropy(normaliseLetterFrequencies(letterFrequencies,total))
            sliceLetterFrequencies.append(letterFrequencies)

        averageScore = totalScore/n

        if averageScore > maxScore:
            maxScore = averageScore
            maxPeriod = n
            maxLetterFrequencies = sliceLetterFrequencies

    return maxPeriod,maxLetterFrequencies

class polyalphabeticSubstitution():

    def __init__(self,cipher):
        self.__cipher = cipher

        self.__period, frequencies = getPeriod(cipher)

        with open("Text analysis/lettersRanked.json", "r") as file:
            self.__idealRank = json.load(file)

        self.__key = []

        # formulates key based on letter frequencies to get a good starting guess
        for frequency in frequencies:

            letterFrequencies = sorted(enumerate(frequency), key=lambda x: x[1], reverse=True)

            alphabet = {}
            for i in range(26):
                alphabet[letterFrequencies[i][0]] = self.__idealRank[i]
            self.__key.append(alphabet)

    def shuffle(self):
        self.__alphabet = self.__key[random.randint(0,self.__period-1)]
        self.__letters = random.sample(range(26), k=2)
        self.__alphabet[self.__letters[0]],self.__alphabet[self.__letters[1]] = self.__alphabet[self.__letters[1]],self.__alphabet[self.__letters[0]]


    def undoShuffle(self):
        self.__alphabet[self.__letters[0]],self.__alphabet[self.__letters[1]] = self.__alphabet[self.__letters[1]],self.__alphabet[self.__letters[0]]

    def decipher(self):
        plainText = []

        for i in range(len(self.__cipher)):
            plainText.append(self.__key[i%self.__period][self.__cipher[i]])

        return plainText
