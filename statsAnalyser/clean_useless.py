import os
import sys
import shutil

dataset_path = "BritishNationalCipherChallenge" 
new_dataset_path = "nccData" 
# os.mkdir("nccData")
# os.remove("nccData")
# sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
for item in os.listdir(dataset_path):
    if item.isalpha():
        continue # we want the year
    elif '.' in item:
        # we don't want the outer files
        continue
    else:
        year_path = os.path.join(dataset_path, item)
        new_year_path = os.path.join(new_dataset_path, item)
        os.mkdir(new_year_path)

        for challenge in os.listdir(year_path):
            if challenge.isalpha() or '.' in challenge:
                continue
            newfolder = os.path.join(new_year_path, challenge)
            oldfolder = os.path.join(year_path, challenge)
            os.mkdir(newfolder)
            for file in os.listdir(oldfolder):
                if file in ["ciphertext.txt", "solution.txt"]:
                    shutil.copyfile(os.path.join(oldfolder, file), os.path.join(newfolder, file))

                

