from formatCipher import intToString
import random

# based on hill climb

# the cipher parameter is the cipher object with methods .decipher etc. It should not be instantiated.
# because similar keys only produce similar plaintexts for the first few characters of a stream cipher, these characters should be prioritised.
# the approach works by gradually feeding in more and more of the plaintext into the cipher.
# It goes up in increments defined by the user. 30 seems to work pretty well for the solitaire cipher.
def hillClimbStream(cipher,cipherText,evaluate,increment,otherArgs=()):
    tryingLength = increment
    cipher = cipher(cipherText[:tryingLength],*otherArgs)

    maxPlainText = cipher.decipher()
    print(intToString(maxPlainText))
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

            while score/tryingLength > -15.5:
                tryingLength += increment
                if tryingLength >= 100:
                    cipher.setCipher(cipherText)
                    plainText = cipher.decipher()
                    actualMaxScore = maxScore = evaluate(cipher.decipher())
                    print(intToString(plainText))
                    print(score)
                    break
                else:
                    cipher.setCipher(cipherText[:tryingLength])

                plainText = cipher.decipher()
                score = actualMaxScore = maxScore = evaluate(plainText)
                print(intToString(plainText))
                print(score)

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
                    for _ in range(random.randint(2,5)):
                        cipher.shuffle()
                withoutClimbing = 0
                plainText = cipher.decipher()
                maxScore = evaluate(plainText)
              
