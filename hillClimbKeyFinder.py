from math import inf

# this hill climb very closely follows from hillClimb.py

# To use this approach, your cipher must have a getKey function

# it is specialised at finding keys for ciphers that have multiple keys
# because there are multiple keys, we don't want this hill climb to run forever, so it has a limit on the number of iterations
# because you can try out multiple keys as the first key, this hill climb outputs its top n keys rather than just one

def hillClimbKeyFinder(cipher,evaluate,iterations,numberOfCandidates):
    candidates = ["placeHolderKey"]*numberOfCandidates
    candidateScores = [-inf]*numberOfCandidates

    count = 0

    # records how long we've been not climbing up the hill
    withoutClimbing = 0

    while True:
        count += 1

        cipher.shuffle()

        plainText = cipher.decipher()
        score = evaluate(plainText)

        # we should only put it in the list if we are better than the first candidate.
        # while a binary search would technically have better time complexity,
        # consider that the vast majority of the time the score will be less than the worst candidate.
        if score > candidateScores[0] and cipher.getKey() not in candidates:
            for i in range(1,numberOfCandidates):
                if score <= candidateScores[i]:
                    candidates[i-1] = cipher.getKey().copy()
                    candidateScores[i-1] = score
                    break
            else:
                candidates[numberOfCandidates - 1] = cipher.getKey().copy()
                candidateScores[numberOfCandidates - 1] = score
                withoutClimbing = 0

        else:
            cipher.undoShuffle()
            withoutClimbing += 1

            # used to break out of local maxima (the effectiveness of the randomly chosen constants 5000 and 10 will
            # vary in effectiveness based on the cipher type, if we wanted to make really good software we might
            # call cipher.getOptimalShuffleAmount() in these places and finely tune each cipher but these seem like good
            # general values)
            if withoutClimbing > 500:

                # we will only check if the count exceeds the iterations if we haven't climbed in a while
                # wouldn't want to stop while we're making progress
                if count >= iterations:
                    return (candidates,candidateScores)

                try:
                    cipher.shake()
                except AttributeError:
                    for _ in range(10):
                        cipher.shuffle()
                withoutClimbing = 0