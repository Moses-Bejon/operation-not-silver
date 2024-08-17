from formatCipher import intToString

# a hill climb attack continuously randomly shuffles the key and only keeps the shuffle if it was superior to the last

# the cipher parameter is the cipher object with methods .decipher etc. It should already be instantiated.
# evaluate parameter is the evaluate function used, should be passed in without the brackets of course.
# (evaluateQuadgramFrequencies from evaluate is performing quite well here)
def hillClimb(cipher,evaluate):
    maxPlainText = cipher.decipher()
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
            if withoutClimbing > 500:
                try:
                    cipher.shake()
                except AttributeError:
                    for _ in range(10):
                        cipher.shuffle()
                withoutClimbing = 0
                plainText = cipher.decipher()
                maxScore = evaluate(plainText)
