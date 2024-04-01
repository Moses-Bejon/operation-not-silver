import numpy as np

def calc_det(matrix) -> int:
    determinant = np.linalg.det(matrix)
    intDet = int(np.round(determinant))

    return intDet

def is_valid_key(key):
    determinant = calc_det(key) % 26
    return determinant != 0 and np.gcd(determinant, 26) == 1


with open("hill_2x2_keys.txt", "w") as f:
    for a in range(0, 25):
        for b in range(0, 25):
            for c in range(0, 25):
                for d in range(0, 25):
                    key = [[a, b], [c, d]]
                    if is_valid_key(key):
                        f.write(f"{a} {b} {c} {d}\n")

                    
                    

