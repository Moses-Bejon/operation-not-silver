import numpy as np

class hill():
    def __init__(self, cipher):
        self.__cipher: str = cipher  # The cipherText

    @staticmethod
    def __char_to_int(char: str):
        # Assumes that char isalpha
        return ord(char.lower()) - 97

    @staticmethod
    def __int_to_char(charCode: int):
        # Assumes that charCode is for a lower alpha char starting with 0 as "a" and 25 as "z"
        return chr(charCode + 97)

    @staticmethod
    def __calc_det(matrix) -> int:
        determinant = np.linalg.det(matrix)
        intDet = int(np.round(determinant))

        return intDet

    # Some linear algebra magic that gets the modulo inverse of the key matrix (I honestly have no idea why this works)
    def __mod_matrix_inv(self, matrix):
        # Calculate determinant and round to int
        intDet = self.__calc_det(matrix)

        # Calculate the modulo inverse of the determinant
        det_inv = pow(intDet, -1, 26)

        # Calculate adjugate and round to int
        matrixInv = np.linalg.inv(matrix)
        adjugate = np.round(intDet * matrixInv).astype(int)

        # Multiply by inverse determinant and apply modulus
        moduloMatrixInv = (adjugate * det_inv) % 26

        return moduloMatrixInv

    def decipher(self, cipher_text, key):
        # Note that the decypher method always assumes that the key is invertable and that the cyphertext is the correct size
        # key should be a np array

        n = len(key)
        cipher_text = cipher_text.lower().replace(" ", "")
        plain_text = ""

        key_inverse = self.__mod_matrix_inv(key)

        # Iterates over n sized chunks of cyphertext to decode, I'll call each chunk a "word" because that sounds cool and no-one can stop me.
        for i in range(0, len(cipher_text), n):
            # Turning each word into an n sized matrix
            word = [self.__char_to_int(char) for char in cipher_text[i: i + n]]
            word = np.array(word)
            word = word.reshape((n, 1))

            # Getting plaintext from dot product and then mod 26
            result = np.dot(key_inverse, word)

            # converting each character in row into characters
            for char in result:
                charCode = int(round(char[0]))  # annoying numpy floating point fix
                plain_text += self.__int_to_char(charCode % 26)

        return plain_text

    def plainTexts(self):
        self.__key = np.array([[0, 0], [0, 0]])  # n x n matrix

        # read key dictionary file line by line, decoding as the lines are read
        with open("hill_2x2_keys.txt", "r") as f:
            hasKey = True
            while hasKey:
                line = f.readline().strip()
                if line != "":
                    # turn string key into nested list
                    line_list = line.split(" ")
                    self.__key = np.array([[line_list[0], line_list[1]], [line_list[2], line_list[3]]], dtype=int)

                    # decode cyphertext using current key
                    plaintext = self.decipher(self.__cipher, self.__key)

                    yield plaintext
                else:
                    # ends subroutine once no keys are left in file
                    hasKey = False
