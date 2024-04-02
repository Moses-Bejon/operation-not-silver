import random


class doubleColumnarSubstitution():

    def __init__(self, cipher):
        self.__cipher = cipher  # the cipherText
        self.__length = len(self.__cipher)

        self.__setNewKey1Length(2)
        self.__setNewKey2Length(2)

    def shuffle(self):
        if random.random() > 0.5:
            self.__shuffledKey1 = True
            if random.random() > 0.5:
                self.__rollAmount = False
                self.__choices = random.sample(self.__key1, k=2)
                self.__key1[self.__choices[0]], self.__key1[self.__choices[1]] = self.__key1[self.__choices[1]], self.__key1[
                    self.__choices[0]]
            else:
                self.__rollAmount = random.randint(1, self.__key1Length - 1)
                self.__key1 = self.__key1[self.__rollAmount:] + self.__key1[:self.__rollAmount]
        else:
            self.__shuffledKey1 = False
            if random.random() > 0.5:
                self.__rollAmount = False
                self.__choices = random.sample(self.__key2, k=2)
                self.__key2[self.__choices[0]], self.__key2[self.__choices[1]] = self.__key2[self.__choices[1]],self.__key2[self.__choices[0]]
            else:
                self.__rollAmount = random.randint(1, self.__key2Length - 1)
                self.__key2 = self.__key2[self.__rollAmount:] + self.__key2[:self.__rollAmount]

    def shake(self):
        # 10 is our maximum key length because beyond that it takes too long to crack ciphers
        if self.__key1Length <= 10:
            self.__setNewKey1Length(self.__key1Length + 1)
        else:
            self.__setNewKey1Length(2)
            if self.__key2Length <= 10:
                self.__setNewKey2Length(self.__key2Length+1)
            else:
                self.__setNewKey2Length(2)

    def undoShuffle(self):
        if self.__shuffledKey1:
            if self.__rollAmount:
                self.__key1 = self.__key1[self.__key1Length - self.__rollAmount:] + self.__key1[:self.__key1Length - self.__rollAmount]
            else:
                self.__key1[self.__choices[0]], self.__key1[self.__choices[1]] = self.__key1[self.__choices[1]], self.__key1[self.__choices[0]]
        else:
            if self.__rollAmount:
                self.__key2 = self.__key2[self.__key2Length - self.__rollAmount:] + self.__key2[:self.__key2Length - self.__rollAmount]
            else:
                self.__key2[self.__choices[0]], self.__key2[self.__choices[1]] = self.__key2[self.__choices[1]], self.__key2[self.__choices[0]]

    def __setNewKey1Length(self, length):
        self.__key1Length = length
        self.__key1 = list(range(self.__key1Length))
        self.__numberOfFilledRows1, self.__leftOver1 = divmod(self.__length, self.__key1Length)

    def __setNewKey2Length(self,length):
        self.__key2Length = length
        self.__key2 = list(range(self.__key2Length))
        self.__numberOfFilledRows2, self.__leftOver2 = divmod(self.__length, self.__key2Length)

    def decipher(self):
        # this decipher function is really efficient, at the cost of being really unreadable
        plainText1 = ""

        # key 1 decipher
        orderedLongs = self.__key1[:self.__leftOver1]

        lengthLeadingUpTo = {0: 0}
        longNumbers = set(orderedLongs)
        place = 0
        for i in range(1, self.__key1Length):
            if i - 1 in longNumbers:
                place += self.__numberOfFilledRows1 + 1
            else:
                place += self.__numberOfFilledRows1
            lengthLeadingUpTo[i] = place

        for row in range(self.__numberOfFilledRows1):
            for column in self.__key1:
                plainText1 += self.__cipher[lengthLeadingUpTo[column] + row]

        for column in orderedLongs:
            plainText1 += self.__cipher[lengthLeadingUpTo[column] + self.__numberOfFilledRows1]

        # key 2 decipher

        plainText2 = ""

        orderedLongs = self.__key2[:self.__leftOver2]

        lengthLeadingUpTo = {0: 0}
        longNumbers = set(orderedLongs)
        place = 0
        for i in range(1, self.__key2Length):
            if i - 1 in longNumbers:
                place += self.__numberOfFilledRows2 + 1
            else:
                place += self.__numberOfFilledRows2
            lengthLeadingUpTo[i] = place

        for row in range(self.__numberOfFilledRows2):
            for column in self.__key2:
                plainText2 += plainText1[lengthLeadingUpTo[column] + row]

        for column in orderedLongs:
            plainText2 += plainText1[lengthLeadingUpTo[column] + self.__numberOfFilledRows2]

        return plainText2
