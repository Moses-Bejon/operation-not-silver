from itertools import permutations
import numpy as np

def calc_det(matrix) -> int:
    determinant = np.linalg.det(matrix)
    intDet = int(np.round(determinant))

    return intDet

def mod_matrix_inv(matrix):
    intDet = calc_det(matrix)
    det_inv = pow(intDet, -1, 26)

    matrix_inv = np.linalg.inv(matrix)
    adjugate = np.round(intDet * matrix_inv).astype(int)
    modulo_matrix_inv = (adjugate * det_inv) % 26

    return modulo_matrix_inv

class threeByThreeHill():

    def __init__(self,cipher):
        self.__cipher = cipher

        trigrams = {}

        for i in range(len(self.__cipher) // 3):
            trigram = self.__cipher[i * 3:i * 3 + 3]

            try:
                trigrams[tuple(trigram)] += 1
            except KeyError:
                trigrams[tuple(trigram)] = 1

        self.trigramRanking = []
        for trigram,frequency in trigrams.items():
            self.trigramRanking.append((trigram, frequency))

        self.trigramRanking = sorted(self.trigramRanking, key=lambda x: x[1], reverse=True)


    def plainTexts(self):
        for permutation in permutations(self.trigramRanking,3):

            A = permutation[0][0][0]
            B = permutation[0][0][1]
            C = permutation[0][0][2]

            D = permutation[1][0][0]
            E = permutation[1][0][1]
            F = permutation[1][0][2]

            G = permutation[2][0][0]
            H = permutation[2][0][1]
            I = permutation[2][0][2]

            a = (13*A+16*D+5*G)%26
            b = (2*A+22*D+5*G)%26
            c = (9*D+13*G)%26

            d = (13 * B + 16* E + 5 * H)%26
            e = (2 * B + 22 * E + 5 * H)%26
            f = (9 * E + 13 * H)%26

            g = (13 * C + 16* F + 5 * I)%26
            h = (2 * C + 22 * F + 5 * I)%26
            i = (9 * F + 13 * I)%26

            try:
                [[a,b,c],[d,e,f],[g,h,i]] = mod_matrix_inv([[a,b,c],[d,e,f],[g,h,i]])
            except:
                continue

            plainText = []

            for place in range(len(self.__cipher) // 3):
                trigram = self.__cipher[place * 3:place * 3 + 3]
                A = trigram[0]
                B = trigram[1]
                C = trigram[2]

                plainText.append((a*A+b*B+c*C)%26)
                plainText.append((d*A+e*B+f*C)%26)
                plainText.append((g*A+h*B+i*C)%26)
            else:
                yield plainText
