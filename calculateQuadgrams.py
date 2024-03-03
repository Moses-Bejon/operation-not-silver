# that is the most common quadgram so it is the initial state of the window
# yes, the program is technically slightly inaccurate, noone cares
window = "that"
quadgrams = {}

with open("trainingData") as book:
    lines = book.readlines()
    for line in lines:
        for letter in line:
            if letter.isalpha():

                try:
                    quadgrams[window] += 1
                except:
                    quadgrams[window] = 1

                window = window[1:]
                window += letter.lower()

print(quadgrams)

