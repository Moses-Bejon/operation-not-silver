import random

from monoAlphabeticSubstitution import monoAlphabeticSubstitution

class monoAlphaNumericSubstitution(monoAlphabeticSubstitution):
    def __init__(self,cipher):
        super().__init__(cipher)
        self._key = {}
        for i in range(36):
            self._key[i] = i

    def shuffle(self):
        self._letters = random.sample(range(26), k=2)
        self._key[self._letters[0]], self._key[self._letters[1]] = self._key[self._letters[1]], self._key[self._letters[0]]
