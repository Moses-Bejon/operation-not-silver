import random
from formatCipher import intToString

# a hill climb attack continuously randomly shuffles the key and only keeps the shuffle if it was superior to the last

# the cipher parameter is the cipher object with methods .decipher etc. It should already be instantiated.
# evaluate parameter is the evaluate function used, should be passed in without the brackets of course.
# (evaluateQuadgramFrequencies from evaluate is performing quite well here)
def hillClimb(cipher,evaluate):
    maxPlainText = cipher.decipher()
    print(intToString(maxPlainText))
    length = len(maxPlainText)

    maxScore = evaluate(maxPlainText)
    actualMaxScore = maxScore

    count = 0

    # records how long we've been not climbing up the hill
    withoutClimbing = 0

    while True:
        count += 1

        cipher.shuffle()

        plainText = cipher.decipher()

        score = evaluate(plainText)

        # we should only tell the user if we've actually made progress
        if score > actualMaxScore:
            print(intToString(plainText))
            print(score)
            print(count)

            actualMaxScore = score
            maxScore = score
            withoutClimbing = 0

        elif score > maxScore:
            maxScore = score
            withoutClimbing = 0

        else:
            cipher.undoShuffle()
            withoutClimbing += 1

            # used to break out of local maxima (the effectiveness of the randomly chosen constants 5000 and 10 will
            # vary in effectiveness based on the cipher type, if we wanted to make really good software we might
            # call cipher.getOptimalShuffleAmount() in these places and finely tune each cipher but these seem like good
            # general values)
            if withoutClimbing > 5000:
                try:
                    cipher.shake()
                except AttributeError:
                    for _ in range(random.randint(1,3)):
                        cipher.shuffle()
                withoutClimbing = 0
                plainText = cipher.decipher()
                maxScore = evaluate(plainText)

from solitaireArray import solitaireArray
from evaluate import evaluateFrontWeightedQuadgramFrequencies
from formatCipher import stringToInt

deck = "8♦, 9♦, 3♥, K♦, A♥, J♣, 5♥, 6♥, 7♥, 8♥, 9♥, 10♥, 6♣, K♥, 4♦, Q♦, 2♠, 10♣, A♦, 5♠, 10♠, joker A, K♣, 4♠, 7♠, K♠, Q♣, 9♠, J♥, Q♥, 2♥, 7♣, 3♠, 6♠, 8♣, ?, ?, ?, ?, ?, ?, ?, ?, joker B, ?, ?, ?, ?, ?, ?, J♦, ?, 7♦, ?"
deck = deck.split(", ")
print(deck)

cipher = solitaireArray(stringToInt("""
AGXJE SSFKM MJMHX ZGJWB CPCVX EBNDK UQOCE DUTIC NPARQ
PEDIX ZAVYM WZSVT BBVMT HJIGW XZAPJ HJMYN MXRGO RXOWE
ULMJS AAENC WVUYI FQUTR XEDEJ BLWAA DFPBW ZAXJD DZOTM
GSEZG NQWJY MFNWL SLTQD URZVQ RKOTS VDNHY EIITY RRWGC
CSLKS UKHDR LDBZE DXSGV UGMTB NZQJT CBZTT IBWKQ PXUTQ
MZDIH HKWZK SJEEH FBFYP GYSIH OKKOB JFJSN XSIKS NBMTN
IADVT CXYZZ AOKQY WXNIZ JWOFZ VSPQQ GASYU MJDEL MDDHV
ZTNFH MOOLN XAFPE VBHGS TJFMC IFNHZ YCYGG WAQYB UNNHD
WHSLP IBFAP PDNQN DOCNU RXEAI RZNLR XAKVX XAMPU ZOPOK
TJVQK IZDSC NC
""")[:100],deck)


def evaluate(plainText):
    englishEvaluation = evaluateFrontWeightedQuadgramFrequencies(plainText)
    adjacencyEvaluation = cipher.getAdjacencyBonus()
    # print(adjacencyEvaluation/englishEvaluation)
    return adjacencyEvaluation+englishEvaluation

hillClimb(cipher,evaluate)