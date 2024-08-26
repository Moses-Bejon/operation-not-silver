import fastEval_quadgrams
import evaluateQuadgrams
import time

no_of_repeats = 10000 

with open("normal.txt", "r") as f:
    plaintext = f.read().replace("\n", "").replace(" ", "").lower()

plaintext_len = len(plaintext)

print("Plaintext length:", plaintext_len)

print()

print("[ Normal Eval ]")
start_t = time.time()
for _ in range(no_of_repeats):
    fitness = evaluateQuadgrams.evaluateQuadgramFrequencies(plaintext)
end_t = time.time()
print("Fitness:", fitness)
print("Time elapsed:", end_t - start_t)

print()

print("[ Fast Eval ]")
process = fastEval_quadgrams.start_process(plaintext_len)
start_t = time.time()
for _ in range(no_of_repeats):
    fitness = fastEval_quadgrams.evaluateQuadgrams(process, plaintext)
end_t = time.time()
print("Fitness:", fitness)
print("Time elapsed:", end_t - start_t)

fastEval_quadgrams.terminate()