import random
import json

from evaluate import evaluateLetterFrequenciesSubstituted

def getPeriod(cipher,max):

    # lowest possible score
    maxScore = -1

    # trying out different periods to see which fits best
    for n in range(1,max):

        # these are the different slices of the cipher text
        slices = [""]*n

        # populating slices
        for place in range(len(cipher)):
            slices[place%n] += cipher[place]

        # checking fitness of slices
        totalScore = 0
        for slice in slices:
            totalScore += evaluateLetterFrequenciesSubstituted(slice)
        averageScore = totalScore/n

        if averageScore > maxScore:
            maxScore = averageScore
            period = n
            maxSlices = slices

    return period,maxSlices

class polyalphabeticSubstitution():

    def __init__(self,cipher):
        self.__cipher = cipher

        # 100 is probably overkill but why not
        self.__period,self.__slices = getPeriod(cipher,100)

        self.__key = []

        # formulates key based on letter frequencies to get a good starting guess
        for slice in self.__slices:
            letterFrequencies = [['a', 0], ['b', 0], ['c', 0], ['d', 0], ['e', 0], ['f', 0], ['g', 0], ['h', 0], ['i', 0], ['j', 0], ['k', 0], ['l', 0], ['m', 0], ['n', 0], ['o', 0], ['p', 0], ['q', 0], ['r', 0], ['s', 0], ['t', 0], ['u', 0], ['v', 0], ['w', 0], ['x', 0], ['y', 0], ['z', 0]]
            for letter in slice:
                letterFrequencies[ord(letter) - 97][1] += 1
            letterFrequencies = sorted(letterFrequencies,key=lambda x:x[1])
            with open("Text analysis/lettersRanked.json","r") as file:
                idealRank = json.load(file)
            alphabet = {}
            for i in range(26):
                alphabet[letterFrequencies[i][0]] = idealRank[i]
            self.__key.append(alphabet)

    def shuffle(self):
        self.__alphabet = self.__key[random.randint(0,self.__period-1)]
        self.__letters = random.sample("abcdefghijklmnopqrstuvwxyz", k=2)
        self.__alphabet[self.__letters[0]],self.__alphabet[self.__letters[1]] = self.__alphabet[self.__letters[1]],self.__alphabet[self.__letters[0]]


    def undoShuffle(self):
        self.__alphabet[self.__letters[0]],self.__alphabet[self.__letters[1]] = self.__alphabet[self.__letters[1]],self.__alphabet[self.__letters[0]]

    def decipher(self):
        plainText = ""

        for i in range(len(self.__cipher)):
            plainText += self.__key[i%self.__period][self.__cipher[i]]

        return plainText
