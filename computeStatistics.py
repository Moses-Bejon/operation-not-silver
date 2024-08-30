from formatCipher import stringToInt, intToString
from linguisticData import evaluate
import numpy as np
import matplotlib.pyplot as plt

def IOC(ciphertext):    
    letterFrequencies, total = evaluate.getLetterFrequencies(ciphertext)
    ioc = evaluate.getIOC(letterFrequencies, total) # not normalised
    return ioc


ciphertext = "WZEALYESUWCNSZEWLKARHLHTGGFJQURDSLISJSLUKSBJWACYHPTBKWRJHSCMOWTYHJOKWZEUOSISWWXYLKESFGDJGOIYKSDNIXEWHFTHDWSFUUIUKWRBKGSJLFCWHEESWASIHLEWPANJGTYYKWCTUJEXSGNILFGQHLTJ"
# ciphertext = "zebra f"
ciphertext = stringToInt(ciphertext)
print(ciphertext)
evalLetterFreq = evaluate.evaluateLetterFrequenciesUnsubstituted(ciphertext)
print("Monogram fitness", evalLetterFreq)
ioc = IOC(ciphertext)

letterFrequencies, total = evaluate.getLetterFrequencies(ciphertext)
gridPossible = 0 in letterFrequencies
if gridPossible:
    lf = np.array(letterFrequencies)
    lettersWithZeroOccurences = (np.argsort(lf)[:letterFrequencies.count(0)])
    print(intToString(lettersWithZeroOccurences))

# functionality to detect possible polyalphabetic periodic ciphers
def evalOverPeriods(ciphertext, evaluator, maxPeriod=40):
    results = []
    periods = list(str(p) for p in range(1, maxPeriod+1, 1))
    for period in range(1, maxPeriod+1, 1):
        everyNthtext = ciphertext[::period] # array[start:stop:step]
        # print(intToString(everyNthtext))
        results.append(evaluator(everyNthtext))
    
    print(results)
    plt.xlabel("Period")
    plt.ylabel("Result")
    plt.title(evaluator.__name__)
    plt.bar(periods, results )
    plt.show()



evalOverPeriods(ciphertext, evaluate.evaluateLetterFrequenciesUnsubstituted)
evalOverPeriods(ciphertext, IOC)
evalOverPeriods(ciphertext, evaluate.evaluateBigramFrequencies)
evalOverPeriods(ciphertext, evaluate.evaluateQuadgramFrequencies)