import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

import pathlib
import random
from basicEncryptors import cipherTypes
from computeStatistics import getStatistics
import pandas as pd
corpusPath = pathlib.Path("..", "linguisticData", "trainingData")
data = []
passageSize = 2500
passages = 10
with open(corpusPath, 'rt', encoding='utf-8') as f:
    text = f.read()
    limit = len(text)
    # print(limit) 
    for i in range(passages):
        start = random.randint(0, limit-passageSize)
        # length = random.randint(passageSize, limit-start)
        length = passageSize
        plaintext = ''.join(text[start:start+length]) # could be lovely to store the length of ciphertext for inspection
        # print(plaintext)
        for cipherType, encryptor in cipherTypes.items():
            # encrypt for all cipher types
            ciphertext = encryptor(plaintext)
            # print(ciphertext)
            entry = {
            'Ciphertext': (ciphertext),
            'CipherType': cipherType
            }
            # give it the stats, merging the dictionary
            entry.update(getStatistics(ciphertext))
            print(entry)
            data.append(entry)


df = pd.DataFrame(data)
df.dropna(axis=0, inplace=True) 
filename = str(passageSize)+ '_length_corpus_data_stats.csv'
df.to_csv(filename, index=False)
    
