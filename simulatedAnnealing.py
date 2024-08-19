import random
import math

def simulatedAnnealing(initialKey, generateCandidateKey, evaluateFitness, decrypt, initialTemp=100.0, coolingRate=0.95, maxIter=1000):
    currentKey = initialKey
    bestKey = currentKey[:]
    bestDecryption = None
    bestScore = float('-inf')

    temp = initialTemp

    for iteration in range(maxIter):
        candidateKey = generateCandidateKey(currentKey)

        # Decrypt with candidate key and evaluate decryption
        decryptedText = decrypt(candidateKey)
        candidateScore = evaluateFitness(decryptedText)

        # accept or reject new score
        deltaScore = candidateScore - bestScore

        if deltaScore > 0 or random.uniform(0, 1) < math.exp(deltaScore/temp):
            currentKey = candidateKey[:]
            if candidateScore > bestScore:
                bestScore = candidateScore
                bestKey = candidateKey[:]
                bestDecryption = decryptedText

        # reduce temp
        temp *= coolingRate

        if iteration % 100 == 0:
            print(f"Iteration: {iteration}, Best Score: {bestScore}, Best Key: {bestKey}")

    return bestKey, bestDecryption

