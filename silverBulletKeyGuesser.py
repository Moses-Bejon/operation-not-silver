from formatCipher import intToString,stringToInt
from evaluate import evaluateQuadgramFrequencies
from itertools import combinations

validWords = set()

with open("linguisticData/9letterDictionary", "r") as dictionary:
    for line in dictionary.readlines():
        validWords.add(tuple(stringToInt(line.strip())))

def subtract(a,b):
    return a - b

def add(a,b):
    return a + b

def runningKey(ciphertext,key,operation):
 plainText = []
 for i in range(len(ciphertext)):
     p = ciphertext[i]
     k = key[i]
     plainText.append(operation(p,k) % 26)
 return plainText

cipherText = "LYPGFFFOL".lower()
integerCipherText = []

for character in cipherText:
    integerCipherText.append(ord(character)-97)

keys = [
    "churchill",
    "misswarne",
    "elizabeth",
    "holocaust",
    "anschluss",
    "luftwaffe",
    "mussolini",
    "abcdefghi",
    "aycdefnki",
    "weltkrieg",
    "kurskline",
    "liverpool",
    "roosevelt",
    "thefuhrer",
    "georgesix",
    "coastline"
]

def tryKey(key):
    global keys

    keys = [key.lower()]
    tryAll()

def tryAll():
    integerKeys = []
    for key in keys:
        integerKey = []
        for character in key:
            integerKey.append(ord(character)-97)
        integerKeys.append(integerKey)

    possibleTexts = []
    for key in integerKeys:
        possibleTexts.append((runningKey(integerCipherText, key,subtract),
                              "key: \""+intToString(key)+"\""))
        possibleTexts.append((runningKey(integerCipherText[::-1], key, subtract),
                              "reversed cipher, key: \""+intToString(key)+"\""))
        possibleTexts.append((runningKey(key,integerCipherText,subtract),
                              "plainText: \""+intToString(key)+"\""))
        possibleTexts.append((runningKey(key, integerCipherText[::-1], subtract),
                              "reversed cipher, plainText: \""+intToString(key)+"\""))
        possibleTexts.append((runningKey(integerCipherText, key, add),
                              "enciphered with subtraction, key: \""+intToString(key)+"\""))
        possibleTexts.append((runningKey(integerCipherText[::-1], key, add),
                              "enciphered with subtracted, reversed cipher, key: \""+intToString(key)+"\""))

    possibleTextsWithShifts = []
    for text,description in possibleTexts:
        for shift in range(26):
            shiftedText = []
            for character in text:
                shiftedText.append((character+shift)%26)
            possibleTextsWithShifts.append((shiftedText,description + " shift: " + str(shift)))

    textsWithScores = []

    for text,description in possibleTextsWithShifts:
        score = evaluateQuadgramFrequencies(text)

        # checking to see if any substrings of the text are in the dictionary
        for start,end in combinations(range(10), r=2):
            if tuple(text[start:end]) in validWords:
                score += 6*(end-start)

        textsWithScores.append((text,score,description))

    textsWithScores = sorted(textsWithScores,key=lambda x:x[1],reverse=True)

    print("top 10 decryptions:")
    for text,score,description in textsWithScores[:10]:
        print(intToString(text),score," - ",description)

tryAll()