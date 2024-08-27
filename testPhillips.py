# cd linguisticData
# python -u "c:\Users\merch\OneDrive - Magdalen College School\A-level CS code\operation-not-silver\testPhillips.py" 
from gridCiphers.phillips import Phillips, intToString, stringToInt
from hillClimb import hillClimbWithMargin, hillClimb
from linguisticData.evaluate import evaluateQuadgramFrequencies, evaluateBigramFrequencies, getLetterFrequencies,getIOC
from simulatedAnnealing import simulatedAnnealing
# cipherString = '''I took a pill down in Ibiza to try and show Avicii I was cool One day I forgot it all holy moly i left 
# and then i tried to write produce read books downloaded papers and cds and ended up with painting until i did a textbook question or ex red level
# '''
cipherString = """
DWCFPHQAZAXMZZLZPLYARDZDMEHHDUUGLFGZPSKMFDWLHOIKIHRFOM
TLCQXCDZPCSLBREHQQZKDLNMAQLFEABIGVZHSMTNMWXBSASBZCWUKU
DGHSOZFHQAFQDHFLOAKRATQSLZLLZTZKMLQLFKAAIVBDFHULICCGZF
CBOAKFCATTILKVTALQLQDHIUULRIKUSLPZIQGKHCFQSZUGLZMZGMSO
WQVWQSZQLGDHCCGWPSOALCGFDFHMLTHQSWCLMAMZHZLYOCVZZICUDU
VHGDLHAWGHQCWLBICGHNRMGPLYWQLQSELHWULGLPHIHGUANGKACGBQ
LTGKWCRNTLRLWYVBLMLHGGKGRGAHIGDZHKGMSDBCOSZSHQNZKQVASZ
AVFHQDOUGBIIWKZFH"""
# cipherText = ("ijk")
# phillips = Phillips(cipherText, keyword="RHYMES")
# print(phillips.decipher())

def evaluate(plaintext):
    bigramScore = evaluateBigramFrequencies(plaintext)
    quadgramScore = evaluateQuadgramFrequencies(plaintext)
    letterFreq, _ = getLetterFrequencies(plaintext)
    iocScore = getIOC(letterFreq, len(plaintext))

    totalScore = bigramScore + 2*quadgramScore + 2 * iocScore
    return totalScore

hillClimb(Phillips(cipherString), evaluateQuadgramFrequencies)
# hillClimbWithMargin(Phillips(cipherString), evaluateQuadgramFrequencies)

# p = Phillips(cipherString)
# key, decryption = simulatedAnnealing(
#     p.generateKey(),
#     lambda genKey: p.shuffle(),
#     lambda dec: evaluateQuadgramFrequencies(p.decipher()),
#     p.decipher,
#     initialTemp=100,
#     maxIter=20000
# )

# print(f'Best key: {key}')
# print(f'Best decrypt: {intToString(decryption)}')


