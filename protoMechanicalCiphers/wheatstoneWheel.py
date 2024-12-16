import json
from math import inf

from monoAlphabeticSubstitution import monoAlphabeticSubstitution
from formatCipher import stringToInt,intToString
from evaluate import evaluateQuadgramFrequencies

def stringToIntWithSpace(cipher):
    formattedCipher = []
    for letter in cipher:
        if letter.isalpha():
            formattedCipher.append(ord(letter.lower())-97)
        elif letter == ' ':
            formattedCipher.append(26)
    return formattedCipher

def encrypt(key,plainText):

    longHandPosition = 0
    shortHandPosition = 0

    cipherText = []

    for character in plainText:
        lengthAlongWheelToMove = (character - longHandPosition)%27

        shortHandPosition = (shortHandPosition + lengthAlongWheelToMove)%26
        longHandPosition = character

        cipherText.append(key[shortHandPosition])

    return cipherText

class wheatstoneWheel(monoAlphabeticSubstitution):

    def __init__(self,cipher):
        self.__cipher = cipher

        with open("Text analysis/wheatstoneShiftTrigrams.json","r") as file:
            self.__wheatstoneShiftTrigramsHashmap = json.load(file)

        super().__init__(cipher)

    def keyFinderEvaluator(self,solution):
        score = 0

        window = solution[:4]
        for i in solution[4:]:
            first = window[0]

            score += self.__wheatstoneShiftTrigramsHashmap[
                ((window[1] - first) % 26) * 26 ** 2 + ((window[2] - first) % 26) * 26 + ((window[3] - first) % 26)]

            window.pop(0)
            window.append(i)

        return score

    def setKey(self,key):
        self._key = {}
        for i,character in enumerate(key):
            self._key[character] = i

    def decipherEnglish(self):

        maxPlainText = []
        maxPlainTextScore = -inf

        for i in range(26):
            charnum = 0
            letternum = 26
            plainText = []
            for character in self.__cipher:
                move = (26 - charnum + self._key[character] + i) % 26
                if move == 0:
                    move = 26
                charnum = self._key[character] + i
                letternum = (letternum + move) % 27
                plainText.append(letternum)

            score = evaluateQuadgramFrequencies([i for i in plainText if i != 26])
            if score > maxPlainTextScore:
                maxPlainText = plainText
                maxPlainTextScore = score

        return maxPlainText
