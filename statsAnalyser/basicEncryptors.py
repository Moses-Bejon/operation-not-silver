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
cipherTypes = {'monoalphabetic substitution': monosub}