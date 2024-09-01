import random

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

        elif score > maxScore or (score > maxScore-length*0.2 and random.random() > 0.5):
            maxScore = score
            withoutClimbing = 0

        else:
            cipher.undoShuffle()
            withoutClimbing += 1

            if withoutClimbing >= 10000:
                try:
                    cipher.shake()
                except AttributeError:
                    for _ in range(5):
                        cipher.shuffle()
                withoutClimbing = 0
                plainText = cipher.decipher()
                maxScore = evaluate(plainText)
