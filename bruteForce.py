from math import inf
from formatCipher import intToString

def bruteForce(cipher,evaluate):
    maxScore = -inf

    for plainText in cipher.plainTexts():
        score = evaluate(plainText)

        # we should only tell the user if we've made progress
        if score > maxScore:
            print(intToString(plainText))
            print(score)
            maxScore = score
