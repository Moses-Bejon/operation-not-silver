import os
import sys
import pandas as pd


'''Thanks ChatGPT!'''
# Define the path to the 2023 dataset folder
dataset_path = "nccData" 

# Adjust to your local path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
from statsAnalyser.computeStatistics import getStatistics

# Create a list to store the data
data = []
def remove_name_variations(cipher_type):
    cipher_type = cipher_type.replace("cipher: ", "")
    cipher_type = cipher_type.replace("cipher", "")
    cipher_type = cipher_type.strip()
    name_variations = {
        "monoalphabetic substitution": ["Caesar shift", "affine","atbash", 
                                        "keyword substitution", "keyed substitution", 
                                        "monoalphabetic substitution"],
        "Vigenere": ["Vigenere"],
        "clock": ["clock"],
        # "Hill": ["Hill"],
        "columnar transposition": ["columnar transposition"]
    }
    for group_name, names in name_variations.items():
        for name in names:
            if name in cipher_type:
                print(group_name)
                return group_name
    return cipher_type
def load_challenge(year_path, challenge_code):
    challenge_path = os.path.join(year_path, challenge_code)
    # Check for the files we need (ciphertext.txt and solution.txt)
    ciphertext_file = os.path.join(challenge_path, 'ciphertext.txt')
    solution_file = os.path.join(challenge_path, 'solution.txt')
    print(challenge_path)
    # Read ciphertext
    if os.path.exists(ciphertext_file):
        with open(ciphertext_file, 'r', encoding="utf-8") as cf:
            ciphertext = cf.readlines() #TODO:  challenges before 2021 have no title so htis strips the real ciphertext. but unlikely
            # print(ciphertext_file, ciphertext)
            if len(ciphertext) > 1:
                ciphertext = ciphertext[1:]
            # try: 
            #     ciphertext = cf.readlines()[1:] #TODO:  challenges before 2021 have no title so htis strips the real ciphertext. but unlikely
            # except UnicodeDecodeError:
            #     print("Weird characters, skipped")
            #     return
            
            ciphertext = ''.join(ciphertext).strip()  # Read and clean up newlines/whitespace
    else:
        print("No ciphertext file found.")
        return
    # Read cipher type from the first line of solution.txt
    if os.path.exists(solution_file):
        with open(solution_file, 'r', encoding="utf-8") as sf:
            cipher_type = sf.readline().strip()  # Only grab the first line
    else:
        print("No solution.txt file found.")
        return

    # Append the results to the data list
    # ciphertext = ciphertext.strip(' \n')
    # TODO: morse code has got absolutely no clue and gets stripped in stringToInt
    cipher_type = remove_name_variations(cipher_type)
    entry = {
        'Ciphertext': (ciphertext),
        'CipherType': cipher_type
    }
    print(cipher_type)
    print(len(ciphertext), 'LEN')
    if len(ciphertext) <= 1:
        print("Something is wrong. Might be a type of code.")
    else:
        # give it the stats, merging the dictionary
        entry.update(getStatistics(ciphertext))
        # print(entry)
        data.append(entry)


def generateYearsCSV(start, end):
    for year in range(start, end+1):
        year_path = os.path.join(dataset_path, str(year))
        for challenge in os.listdir(year_path):
            if len(challenge) <= 3 and ('A' in challenge or 'B' in challenge): # skip extra files with file extension .mp3 or .jpg
                load_challenge(year_path, challenge)
    # Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(data)
    df.dropna(axis=0, inplace=True) 
    filename = str(start) +'-'+ str(end) + '_ciphertext_data_stats.csv'
    # Output the data to a CSV or use it directly in your processing
    df.to_csv(filename, index=False)
    print(df.tail()["CipherType"])  # To check the first few rows
    return filename

