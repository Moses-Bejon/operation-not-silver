import random
import math
from formatCipher import intToString


def simulatedAnnealing(initialKey, generateCandidateKey, evaluateFitness, decrypt, initialTemp=100.0, coolingRate=0.95,
                       maxIter=1000):
    currentKey = initialKey[:]
    bestKey = currentKey[:]
    bestDecryption = None
    bestScore = float('-inf')

    temp = initialTemp

    # iterations without any improvement in score
    noImprovementCount = 0

    # threshold to decide if algorithm stuck at a local optimum
    stuckThreshold = 10000

    for iteration in range(maxIter):
        candidateKey = generateCandidateKey(currentKey)

        # Decrypt with candidate key and evaluate decryption
        decryptedText = decrypt(candidateKey)
        candidateScore = evaluateFitness(decryptedText)

        # accept or reject new score
        deltaScore = candidateScore - bestScore

        if deltaScore > 0 or random.uniform(0, 1) < math.exp(deltaScore / temp):
            currentKey = candidateKey[:]
            noImprovementCount = 0
            if candidateScore > bestScore:
                bestScore = candidateScore
                bestKey = candidateKey[:]
                bestDecryption = decryptedText

                # Print only when progress is made
                print(f"Iteration: {iteration}, Best Score: {bestScore}, Decryption: {intToString(bestDecryption)}")
        else:
            noImprovementCount += 1

        # check if stuck in local optimum
        if noImprovementCount > stuckThreshold:
            # Debug print
            print(f'stuck in local optimum at iteration {iteration}...')

            # Reset temp and key and score
            temp = initialTemp

            currentKey = initialKey[:]
            random.shuffle(currentKey)

            bestScore = float('-inf')

            # Reset counter
            noImprovementCount = 0

            # Debug print
            print(f'New Key: {currentKey}')

        # reduce temp
        temp *= coolingRate

    return bestKey, bestDecryption
