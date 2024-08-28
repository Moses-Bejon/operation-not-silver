from evaluate import evaluateQuadgramFrequencies
import random
from formatCipher import robustStringToInt

with open("../../Text analysis/trainingData", "r") as file:
    file = file.readlines()

    iterations = 0
    while True:
        iterations += 1
        lines = random.randint(0,161000)
        toEvaluate = []
        for i in range(lines,lines+1):
            toEvaluate += robustStringToInt(file[i])

        try:
            if evaluateQuadgramFrequencies(toEvaluate)/len(toEvaluate) < -15.5:
                print(iterations)
                for i in range(lines,lines+2):
                    print(file[i])
                print(evaluateQuadgramFrequencies(toEvaluate)/len(toEvaluate))
                input()
        except:
            pass

