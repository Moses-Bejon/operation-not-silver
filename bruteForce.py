from math import inf
def bruteForce(cipher,evaluate):
    maxScore = -inf

    for plainText in cipher.plainTexts():
        score = evaluate(plainText)

        # we should only tell the user if we've made progress
        if score > maxScore:
            print(plainText)
            print(score)
            maxScore = score
