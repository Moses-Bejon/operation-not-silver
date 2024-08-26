import numpy as np
from multiprocessing import shared_memory
import subprocess

def __create_shared_array(arr):
    shm = shared_memory.SharedMemory(create = True, size = arr.nbytes)

    shared_iqf = np.ndarray(arr.shape, dtype = np.float64, buffer = shm.buf)

    np.copyto(shared_iqf, arr)

    return shm

def evaluateQuadgrams(process: subprocess.Popen, plaintext):
    #send plaintext to the process using stdin
    process.stdin.write(f"{plaintext}\n")
    process.stdin.flush()
    
    return float(process.stdout.readline())

def start_process(plaintext_len):
    return subprocess.Popen(
        ["./evaluateQuadgrams", iqf_shm.name, str(plaintext_len)],
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True
    )
    
def terminate():
    iqf_shm.close()
    iqf_shm.unlink()

def calculateHash(quadgram):
    return (ord(quadgram[0]) - 97) * 17576 + (ord(quadgram[1]) - 97) * 676 + (ord(quadgram[2]) - 97) * 26 + (ord(quadgram[3]) - 97)

no_of_quadgrams = 456976
idealQuadgramFrequencies = np.full(no_of_quadgrams, -25.0, dtype = np.float64)

with open("quadgram proportions.txt") as f:
    line = f.readline()
    while line != "":
        quadgram, frequency = line.split(" ")
        idealQuadgramFrequencies[calculateHash(quadgram)] = float(frequency)
        line = f.readline()

iqf_shm = __create_shared_array(idealQuadgramFrequencies)

if __name__ == "__main__":
    plaintext = "helloworldthisisapieceofplaintexttobeevaluated"
    process = start_process()

    print("fitness:", evaluateQuadgrams(process, plaintext, len(plaintext)))

    terminate()

