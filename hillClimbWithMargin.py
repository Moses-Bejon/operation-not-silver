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

        elif score > maxScore or (score > maxScore-length*0.1 and random.random() > 0.5):
            maxScore = score

        else:
            cipher.undoShuffle()

from verticalTwoSquare import verticalTwoSquare
from evaluate import evaluateQuadgramFrequencies
from formatCipher import stringToInt

cipher = verticalTwoSquare(stringToInt("""
XCSOKGSOMYHBMQBWSOLYEWLYMXPRHZSTNZQCMZLGMBMPWILWQQBPVG
ICHHVPPRQKIQMAMHMZXBHZAYHUHDBWVDTIMBAYNYVDNTIYUHHTKEHP
PGCNSCEVXCSOSMKXPWIRACTTHEQCVDSNNZELDBIYPGYTKEITKGSOLZ
OWHTMFLZHELOITDIITWRACTOSCMZSOLGFLRDLYAXSOLYHFLYSOAZTB
TWIYDBMXMKIQBXRXVTNLMNKZSOPYPCHTTRMWQQIQTBVGTWKZTBVGIY
YBIXPZNLQZMZMBPPBINTICMBKGBISIDZVDMOKGDWNTHEKEDUVDZQ
"""))

hillClimb(cipher,evaluateQuadgramFrequencies)