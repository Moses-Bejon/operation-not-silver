import fastEval_quadgrams
import evaluateQuadgrams
import time


with open("long.txt", "r") as f:
    plaintext = f.read().replace("\n", "")

plaintext_len = len(plaintext)

print("Plaintext length:", plaintext_len)

print()

print("[ Normal Eval ]")
start_t = time.time()
print("Fitness:", evaluateQuadgrams.evaluateQuadgramFrequencies(plaintext))
end_t = time.time()
print("Time elapsed:", end_t - start_t)

print()

print("[ Fast Eval ]")
start_t = time.time()
print("Fitness:", fastEval_quadgrams.evaluateQuadgrams(plaintext, plaintext_len))
end_t = time.time()
print("Time elapsed:", end_t - start_t)

fastEval_quadgrams.terminate()