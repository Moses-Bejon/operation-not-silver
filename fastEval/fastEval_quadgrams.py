import numpy as np
from multiprocessing import shared_memory
import subprocess

def __create_shared_array():
    shm = shared_memory.SharedMemory(create = True, size = idealQuadgramFrequencies.nbytes)

    shared_iqf = np.ndarray(idealQuadgramFrequencies.shape, dtype = np.float64, buffer = shm.buf)

    np.copyto(shared_iqf, idealQuadgramFrequencies)

    return shm, idealQuadgramFrequencies.nbytes

def evaluateQuadgrams(plaintext: str, plaintext_len: int):
    return float(
        subprocess.run(
            ["./evaluateQuadgrams", shm.name, no_of_quadgrams_str, memory_size_str, plaintext, str(plaintext_len)], 
            capture_output = True
        ).stdout
    )
    
def terminate():
    shm.close()
    shm.unlink()

def calculateHash(quadgram):
    return (ord(quadgram[0]) - 97) * 17576 + (ord(quadgram[1]) - 97) * 676 + (ord(quadgram[2]) - 97) * 26 + (ord(quadgram[3]) - 97)


no_of_quadgrams = 26 ** 4
no_of_quadgrams_str = str(no_of_quadgrams)
idealQuadgramFrequencies = np.full(no_of_quadgrams, -25.0, dtype = np.float64)

with open("quadgram proportions.txt") as f:
    line = f.readline()
    while line != "":
        quadgram, frequency = line.split(" ")
        idealQuadgramFrequencies[calculateHash(quadgram)] = float(frequency)
        line = f.readline()

shm, memory_size = __create_shared_array()
memory_size_str = str(memory_size)

if __name__ == "__main__":
    plaintext = "helloworldthisisapieceofplaintexttobeevaluated"
    print("fitness:", evaluateQuadgrams(plaintext, len(plaintext)))

    terminate()

