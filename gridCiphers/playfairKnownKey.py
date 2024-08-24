# Create digraphs from ciphertext
def createDigraphs(cipher):
    digraphs = []
    i = 0
    while i < len(cipher):
        a = cipher[i]
        if i + 1 < len(cipher):
            b = cipher[i + 1]
            # if both letters are the same, diagraph = 'x'
            if a == b:
                digraphs.append(a + 'x')
                i += 1
            else:
                digraphs.append(a + b)
                i += 2
        else:
            digraphs.append(a + 'x')
            i += 1
    return digraphs


class playfair:
    def __init__(self, cipherText, key):
        self.__cipherText = cipherText
        self.__key = key
        self.__keySquare = self.createSquares(key)

    # Currently works for 5x5 squares
    def createSquares(self, key):
        keySquare = []
        usedLetters = set()
        for letter in key:
            if letter not in usedLetters and letter != 'j':
                keySquare.append(letter)
                usedLetters.add(letter)
        for letter in "abcdefghiklmnopqrstuvwxyz":  # No 'J' in 'standard' cipher
            if letter not in usedLetters:
                keySquare.append(letter)
                usedLetters.add(letter)
        # return matrix
        return [keySquare[i * 5:(i + 1) * 5] for i in range(5)]

    # Find position of letters in the square
    def findPosition(self, letter):
        for row in range(5):
            for col in range(5):
                if self.__keySquare[row][col] == letter:
                    return row, col

    def decodePair(self, digraph):
        a, b = digraph
        row_a, col_a = self.findPosition(a)
        row_b, col_b = self.findPosition(b)

        if row_a == row_b:
            # same row= shift columns left
            return self.__keySquare[row_a][(col_a - 1) % 5] + self.__keySquare[row_b][(col_b - 1) % 5]
        elif col_a == col_b:
            # same col= shift rows up
            return self.__keySquare[(row_a - 1) % 5][col_a] + self.__keySquare[(row_b - 1) % 5][col_b]
        else:
            # swap columns but keep rows - Rectangle shuffle
            return self.__keySquare[row_a][col_b] + self.__keySquare[row_b][col_a]

    def decipher(self):
        digraphs = createDigraphs(self.__cipherText)
        plainText = ''
        for pair in digraphs:
            plainText += self.decodePair(pair)
        return plainText.replace('x', '')


# key = "GROCEISABDFHKLMNPQTUVWXYZ"
# key = key.lower()
# cipherText = "MDSOASOGTGKCDRBZEQVSKYMHFVIBDSKYMHCOROCEGODGABUICQMRORAOEAIHPEVFHPDMQCXCNDPUMRKBBPASZKGQPLABKENPNBVIQCASYQWBGZGUAEKYKBSHIQBUFSCPVLEQOEGUPBBNEQRFQYQCKSZGDCGUQSSIDCKGOGKRXZEQDKFVSAUCOCLNMRRCHWCMOBVFPDNBLVXCPEDRMHFVPDFVOVRCEAHRFSRLXCZMGQUQBXKGGSOBPUNPMDSHQBUIFNSGDUDUDCOWGSRFYTCYMRDSLTRDBXARZRQGKDQITVPLFVOIASDPQWQRDRXCPEGECRVFEDPLCDSDMCBAIQDQPLCOBNVBOZURBYXCNURQBXNQWSEKQUTCIQAELTFICZEQSHOGHWGENLTMTCPLEKBAUNAEOW"
# cipherText = cipherText.lower()
# playfairCipher = playfair(cipherText, key)
# plainText = playfairCipher.decipher()
# print(plainText)
