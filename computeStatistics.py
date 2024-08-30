from formatCipher import stringToInt, intToString
from linguisticData.evaluate import *
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def IOC(ciphertext, block=1, times_entropy=False):
    original = ciphertext[:]    
    # divide into blocks of size block like madness p.31- IN PROGRESS
    # --------------------------------------------------------
    ciphertext = [
        tuple(ciphertext[start:start+block])
        for start in range(len(ciphertext)//block)
    ]
    print(ciphertext)
    counter = Counter(ciphertext)
    blockFrequencies = counter.values()
    # --------------------------------------------------------
    
    letterFrequencies, total = getLetterFrequencies(original)
    ioc = getIOC(letterFrequencies, counter.total()) # not normalised
    print(ioc)
    if times_entropy:
        entropy = getEntropy(normaliseLetterFrequencies(letterFrequencies,total))
        return entropy*ioc
    return ioc

def IOCTimesEntropy(ciphertext):
    return IOC(ciphertext, times_entropy=True)


# 3x3 hill from madness - to test IOC for n-gram blocks
# ciphertext = "RBC GUG KAG EQY GQM IXR DEV ISN ZAV OAD FDQ TST BCL"

# a random vigenere with key length 4
ciphertext = "WZEALYESUWCNSZEWLKARHLHTGGFJQURDSLISJSLUKSBJWACYHPTBKWRJHSCMOWTYHJOKWZEUOSISWWXYLKESFGDJGOIYKSDNIXEWHFTHDWSFUUIUKWRBKGSJLFCWHEESWASIHLEWPANJGTYYKWCTUJEXSGNILFGQHLTJ"
# ciphertext = "zebra f"
ciphertext = stringToInt(ciphertext)
print(ciphertext)
evalLetterFreq = evaluateLetterFrequenciesUnsubstituted(ciphertext)
print("Monogram fitness", evalLetterFreq)
ioc = IOC(ciphertext)

letterFrequencies, total = getLetterFrequencies(ciphertext)
gridPossible = 0 in letterFrequencies
if gridPossible:
    lf = np.array(letterFrequencies)
    lettersWithZeroOccurences = (np.argsort(lf)[:letterFrequencies.count(0)])
    print(intToString(lettersWithZeroOccurences))

# functionality to detect possible polyalphabetic periodic ciphers
def evalOverPeriods(ciphertext, evaluator, maxPeriod=30):
    results = []
    periods = [] # string, for plt to not do decimals in x axis
    for period in range(1, maxPeriod+1, 1):
        aggregate = 0 # for period of 4, abcd efgh we'll check ioc 4 times for ae, bf, cg, dh
        for starting in range(period):
            everyNthtext = ciphertext[starting::period] # array[start:stop:step]
            if len(everyNthtext) > 0: # how to prevent error with quadgram?? TODO: fix in py
                print(intToString(everyNthtext))
                aggregate += evaluator(everyNthtext) # add the score
            else:
                break
        aggregate /= period # we calculated as many IOCs as the length of the period and averaged
        results.append(aggregate) 
        periods.append(str(period))

    
    # print(results)
    plt.xlabel("Period")
    plt.ylabel("Result")
    plt.title(evaluator.__name__ + " over periods")
    plt.bar(periods, results)
    plt.show()



# evalOverPeriods(ciphertext, evaluateLetterFrequenciesUnsubstituted)
evalOverPeriods(ciphertext, IOC)
evalOverPeriods(ciphertext, IOCTimesEntropy)
# evalOverPeriods(ciphertext, evaluateBigramFrequencies)
# evalOverPeriods(ciphertext, evaluateQuadgramFrequencies)