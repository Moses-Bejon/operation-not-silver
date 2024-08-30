from unidecode import unidecode

# takes cipher string and formats it into array of integers
def stringToInt(cipher):
    formattedCipher = []
    for letter in cipher:
        if letter.isalpha():
            formattedCipher.append(ord(unidecode(letter).lower())-97)
    return formattedCipher

def robustStringToInt(cipher):
    formattedCipher = []
    cipher = unidecode(cipher).lower()
    for letter in cipher:
        if letter.isalpha():
            formattedCipher.append(ord(letter) - 97)
    return formattedCipher

def intToString(cipher):
    formattedCipher = ""
    for letter in cipher:
        formattedCipher += chr(letter+97)
    return formattedCipher
