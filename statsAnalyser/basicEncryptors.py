import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

from formatCipher import cleanString
alphabet = 'abcdefghijklmnopqrstuvwxyz'
def monosub(plaintext):
    plaintext = cleanString(plaintext)
    key = list(alphabet)
    random.shuffle(key)
    plainToCiph = dict(zip(alphabet, key))
    ciphertext = ""
    for char in plaintext:
        ciphertext += plainToCiph[char]
    return ciphertext

def bigramsub(plaintext):
    plaintext = cleanString(plaintext)
    bigramAlphabet = []
    key = []

    for l in alphabet:
        for l2 in alphabet:
            bigramAlphabet.append(l+l2)
            key.append(l+l2)
    random.shuffle(bigramAlphabet)
    plainToCiph = dict(zip(bigramAlphabet, key))
    # print(plainToCiph)
    ciphertext = ""
    for c in range(0, len(plaintext)-1, 2):
        ciphertext += plainToCiph[plaintext[c:c+2]]
    return ciphertext

def transposition(plaintext):
    plaintextList = list(cleanString(plaintext))
    random.shuffle(plaintextList)
    plaintext = ''.join(plaintextList)
    return plaintext

cipherTypes = {'monoalphabetic substitution': monosub,
               'bigram substitution': bigramsub,
               'transposition': transposition}

print(transposition("abcdef"))