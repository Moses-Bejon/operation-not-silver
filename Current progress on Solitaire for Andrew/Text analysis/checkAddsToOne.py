import json

with open("letterFrequenciesSortedNormalised.json","r") as proportions:
    data = json.load(proportions)

total = 0
for datum in data:
    total += datum
print(total)