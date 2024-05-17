import numpy as np

def calc_det(matrix) -> int:
    determinant = np.linalg.det(matrix)
    intDet = int(np.round(determinant))

    return intDet

def is_valid_key(key):
    determinant = calc_det(key) % 26
    return determinant != 0 and np.gcd(determinant, 26) == 1

def mod_matrix_inv(matrix):
    #Calculate determinant and round to int
    intDet = calc_det(matrix)

    #Calculate the modulo inverse of the determinant
    det_inv = pow(intDet, -1, 26)

    #Calculate adjugate and round to int
    matrixInv = np.linalg.inv(matrix)
    adjugate = np.round(intDet * matrixInv).astype(int)

    #Multiply by inverse determinant and apply modulus
    moduloMatrixInv = (adjugate * det_inv) % 26     

    return moduloMatrixInv


#INVERSE KEY GENERATOR
print("[ STARTED ]")
with open("hill_2x2_inv_keys.txt", "w") as f:
    for a in range(0, 25):
        for b in range(0, 25):
            for c in range(0, 25):
                for d in range(0, 25):
                    key = [[a, b], [c, d]]
                    if is_valid_key(key):
                        inv_key = mod_matrix_inv(key)

                        f.write(f"{inv_key[0][0]} {inv_key[0][1]} {inv_key[1][0]} {inv_key[1][1]}\n")
print("[ ENDED ]")
print(">>> All keys have been generated.")
                  

#NORMAL KEY GENERATOR
"""
with open("hill_2x2_keys.txt", "w") as f:
    for a in range(0, 25):
        for b in range(0, 25):
            for c in range(0, 25):
                for d in range(0, 25):
                    key = [[a, b], [c, d]]
                    if is_valid_key(key):
                        f.write(f"{key[0][0]} {key[0][1]} {key[1][0]} {key[1][1]}\n")
"""