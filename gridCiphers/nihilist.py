from random import sample
from time import time
from copy import deepcopy
from threading import Thread
# from hillPackage import evaluater
from linguisticData.evaluate import evaluateQuadgramFrequencies

class Nihilist():
    def __init__(self, cipher):
        self.__cipher: tuple[int] = cipher 
        self.__trials = 0
        self.__results = {}

        self.valid_nums = {11, 12, 13, 14, 15, 21, 22, 23, 24, 25, 31, 32, 33, 34, 35, 41, 42, 43, 44, 45, 51, 52, 53, 54, 55}
    
    #get all possible key lengths based on valid numbers generated by applying key: O(n + n + 25n)
    def generatePossibleKeys(self, key_length):
        key_segments = [[] for _ in range(0, key_length)]

        for i in range(len(self.__cipher)):
            key_segments[i % key_length].append(self.__cipher[i])

        possible_key_vals = []
        
        for seg in key_segments:
            seg_possible_keys = deepcopy(self.valid_nums)
            for val in seg:
                for key in self.valid_nums:
                    if (val - key) not in self.valid_nums: 
                        seg_possible_keys.discard(key)

            possible_key_vals.append(list(seg_possible_keys))

        return possible_key_vals
    
    def getBest_keylengths(self):
        best_key_lens = []
        for n in range(2, 25):
            possible_key_vals = self.generatePossibleKeys(n)
            if [] not in possible_key_vals:
                best_key_lens.append(n)
        
        return best_key_lens

    @staticmethod
    def get_keySquare(keyword: str, ommit = ""):
        keyword = keyword.lower()
        ommit = ommit.lower()

        letters = list("abcdefghijklmnopqrstuvwxyz")
        letters.remove(ommit)

        stripped_keyword = []
        for letter in keyword:
            if letter in letters:
                stripped_keyword.append(letter)
                letters.remove(letter)
        keyword = stripped_keyword

        if len(keyword) < 26:
            return keyword + letters
        else:
            print("keyword too large")
            return False

    @staticmethod
    def print_keySquare(keySquare):
        print("keySquare = [")
        for i in range(0, 20, 5):
            print("  ", end = "")
            for j in range(5):
                print(keySquare[i + j], end = ", ")
            print()
        print("  ", end = "")
        for j in range(4):
            print(keySquare[i + j], end = ", ")
        print(keySquare[24])
        print("]")
    
    def print_key(self, key, keySquare):
        print("key = (", end = "")
        for letter in key[ :-1]:
            print(self.get_char(keySquare, letter - 11) + ", ", end = "")
        print(self.get_char(keySquare, key[-1] - 11) + ")")

    @staticmethod
    def get_char(keySquare, char_index):
        return keySquare[(char_index // 10) * 5 + char_index % 10]

    def decipher(self, keySquare, key: tuple[int]):
        key_len = len(key)

        plain_text = ""
        for i in range(len(self.__cipher)):
            char_index = (cipher_text[i] - key[i % key_len] - 11)

            plain_text += self.get_char(keySquare, char_index)

        return plain_text
    
    @staticmethod
    def swap_letters(keySquare: list, l1, l2):
        i1 = keySquare.index(l1)
        i2 = keySquare.index(l2)

        keySquare[i1], keySquare[i2] = keySquare[i2], keySquare[i1]

        return keySquare
    
    def shuffle(self, keySquare):
        l1, l2 = sample(keySquare, 2)
        return self.swap_letters(keySquare, l1, l2), l1, l2
    
    def shake(self, keySquare):
        for _ in range(2):
            keySquare, _, _ = self.shuffle(keySquare)
        return keySquare

    def new_key(self, possible_key_vals, key_len):
        return tuple(sample(possible_key_vals[i], k = 1)[0] for i in range(key_len))
    
    def hillClimb(self, key_len, ommit = "j", max_trials = 100000, silent = False):
        maxScore = float("-inf")
        curr_maxScore = float("-inf")
        best_plain_text = ""
        best_keySquare = []
        best_key = ()

        possible_key_vals = self.generatePossibleKeys(key_len)
        key = self.new_key(possible_key_vals, key_len)

        keySquare = self.get_keySquare("", ommit)

        start = time()

        idle = 0
        for trials in range(max_trials):
            keySquare, l1, l2 = self.shuffle(keySquare)
            if not trials % 20:
                key = self.new_key(possible_key_vals, key_len)

            plain_text = self.decipher(keySquare, key)

            if plain_text:
                score = evaluateQuadgramFrequencies(plain_text)

                if score > maxScore:
                    maxScore = score
                    curr_maxScore = score
                    best_plain_text = plain_text
                    best_keySquare = deepcopy(keySquare)
                    best_key = key
                    
                    if not silent:
                        print("Score:", maxScore)
                        print("Number of Trials:", trials + 1)
                        print(" >", plain_text)
                        self.print_keySquare(keySquare)
                        self.print_key(key, keySquare)
                        print()
                elif score > curr_maxScore:
                    curr_maxScore = score
                else:
                    self.swap_letters(keySquare, l1, l2)
                    idle += 1

                    if idle > 1000:
                        idle = 0
                        keySquare = self.shake(keySquare)

                        curr_maxScore = evaluateQuadgramFrequencies(plain_text)

        end = time()

        if not silent:
            print()
            print("[ RESULTS ]")
            print("-------------------------------------------------------------------------------")
            print("Time elapsed:", end - start)
            print("Max score achieved:", maxScore)
            print("Trials:", trials + 1)
            print(" >", best_plain_text)
            print("------------------")
            print("Best ", end = "")
            self.print_keySquare(best_keySquare)
            print("Best ", end = "")
            self.print_key(best_key, best_keySquare)


        self.__trials += trials + 1

        self.__results[key_len] = {
            "bestscore": maxScore, 
            "bestplaintext": best_plain_text, 
            "bestkeysquare": deepcopy(best_keySquare), 
            "bestkey": best_key
        }

    def auto_hillClimb(self, ommit = "j", max_trials = -1):
        self.__trials = 0

        best_key_lens = self.getBest_keylengths()

        if best_key_lens == []:
            print(">>> Error: No possible key lengths found")
            return None
        
        #longer ciphertext generally don't need to be run that many times
        if max_trials == -1:
            max_trials = 1000000 // len(cipher_text) + 2000

        print("[ PROGRAM STARTED ]")

        start = time()

        hillClimb_threads = []
        for key_len in best_key_lens:
            hillClimb_threads.append([Thread(target = self.hillClimb, args = (key_len, ommit, max_trials, True, )), key_len])
            hillClimb_threads[-1][0].start()
            print(f">>> Thread for key length {key_len} started")
        
        print("\nrunning...\n")
        
        for thread_data in hillClimb_threads:
            thread_data[0].join()
            print(f">>> Thread for key length {thread_data[1]} has ended")

        end = time()

        print("[ PROGRAM ENDED ]")

        #since dictionaries are ordered, the smallest keylen is always outputted if two of the same score is acheived
        best_score = (0, float("-inf"))
        for key_len, result in self.__results.items():
            if result["bestscore"] > best_score[1]:
                best_score = (key_len, result["bestscore"])
        
        best_keylen = best_score[0]
        best_result = self.__results[best_keylen]

        print()
        print("[ RESULTS ]")
        print("-------------------------------------------------------------------------------")
        print("Time elapsed:", end - start)
        print("Max score achieved:", best_result["bestscore"])
        print("Total trials:", self.__trials)
        print(" >", best_result["bestplaintext"])
        print("------------------")
        print("Best ", end = "")
        self.print_keySquare(best_result["bestkeysquare"])
        print("Best ", end = "")
        self.print_key(best_result["bestkey"], best_result["bestkeysquare"])
        print("Best keylength:", best_keylen)

#made this to help with loading in and formatting the ciphertext
#loads .txt files 
def load_ciphertext(path):
    with open(path, "r") as f:
        cipher_text = ""
        while True:
            line = f.readline().strip()

            if line == "":
                break
            else:
                cipher_text += line + " "
    return cipher_text.strip()


if __name__ == "__main__":
    #cipher_text = load_ciphertext("nihilist_inp.txt")
    cipher_text = "34 80 57 87 47 63 47 25 88 56 78 76 44 58 24 60 65 57 45 34 86 44 58 95 75 63 44 86 25 67 57 57 45 36 57 43 77 86 87 47 34 89 27 56 65 77 66 33 50 24 66 86 58 43 65 50 36 77 65 77 64 65 56 36 60 64 64 77 57 67 55 66 78 75 63 54 69 44 88 64 65 67 36 57 47 67 55 67 63 76 67 47 89 74 75 75 66 66 27 90 68 74 67 35 59 25 88 86 65 44 54 69 66 68 55 75 45 33 67 56 76 65 86 55 35 48 47 89 74 56 73 67 47 53 60 86 56 76 37 60 44 96 56 65 66 56 79 43 58 75 64 73 37 47 56 67 78 87 43 44 59 56 88 65 78 46 66 50 55 58 87 54 47 34 79 43 89 74 56 76 53 48 27 57 75 56 75 37 46 34 79 77 87 63 37 78 25 97 74 58 84 53 48 56 76 56 55 53 37 49 25 57 65 87 45 37 47 24 67 57 75 56 44 69 64 76 56 87 63 35 47 55 77 78 67 45 34 48 46 99 77 65 55 37 47 44 80 68 75 67 66 66 25 77 78 87 45 34 48 55 89 86 58 43 53 80 33 67 78 75 76 76 50 24 68 58 75 75 66 48 24 60 88 86 66 76 78 56 57 75 94 64 57 60 23 60 55 78 47 66 50 24 77 56 87 86 53 57 63 58 56 78 46 35 57 63 60 55 56 46 37 47 53 57 56 87 45 57 49 25 59 87 58 64 43 76 24 60 94 56 77 63 50 47 89 74 56 45 75 67 55 89 75 78 57 37 47 26 58 55 58 43 65 50 36 77 56 87 86 54 79 44 88 65 84 66 44 67 47 80 65 55 44 44 79 44 96 56 95 63 37 78 25 77 78 87 45 34 48 55 89 77 75 45 65 67 47 89 74 56 53 37 56 25 80 87 58 77 65 59 43 67 55 65 56 66 48 24 60 54 87 63 35 46 34 69 87 86 84 53 67 36 76 75 87 44 35 69 34 89 56 86 53 67 59 43 60 54 75 76 54 78 47 60 95 54 47 34 79 43 58 54 75 44 65 79 56 77 64 56 57 54 86 25 80 87 58 76 53 48 53 90 66 77 64 46 67 43 67 94 56 46 34 57 64 80 88 84 47 57 79 43 58 55 56 56 37 47 26 88 58 54 76 53 48 36 67 86 56 53 44 49 25 77 78 67 47 67 47 56 68 88 87 53 37 47 25 58 86 84 45 46 67 34 79 77 97 77 63 50 47 89 74 56 44 35 76 27 57 87 86 53 44 49 25 89 58 64 45 36 80 24 77 78 68 76 53 48 53 57 58 68 44 35 78 55 60 54 87 63 35 67 47 96 56 86 76 54 60 34 89 75 58 67 45 89 56 76 56 64 54 57 89 26 58 87 56 56 66 67 63 58 86 95 63 37 87 25 57 56 95 47 34 68 44 80 68 88 67 36 48 24 66 97 57 64 34 48 36 89 75 58 67"
    cipher_text = tuple([int(letter) for letter in cipher_text.split(" ")])
    
    nihilist_cipher = Nihilist(cipher_text)

    #Automatic method
    nihilist_cipher.auto_hillClimb()

    #Manual methods
    #print(nihilist_cipher.getBest_keylengths())
    #nihilist_cipher.hillClimb(7)

