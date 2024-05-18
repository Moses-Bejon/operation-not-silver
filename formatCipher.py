# takes cipher string and formats it into array of integers
def formatCipher(cipher):
    formattedCipher = []
    for letter in cipher:
        if letter.isalpha():
            formattedCipher.append(ord(letter.lower())-97)
    return formattedCipher
