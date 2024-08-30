#Parallel hill climb is intended for ciphers that require parallel testing of multiple possablities
#see Nilist cipher for an implamented version of this template

from time import time
from threading import Thread

import evaluater.evaluate

#change as needed for each cipher
auto_ciel = 2000000
auto_floor = 2000

class Parallel_HillClimb:
    def __init__(self, cipher):
        self.__cipher = cipher 
        self.__trials = 0
        self.__worker_threads = []
        self.__results = {}

    def decipher(self):
        #decipher to plaintext here
        plain_text = self.__cipher

        return plain_text
    
    def shuffle(self, key):
        new_key = key #shuffle key here

        return new_key, key #shuffled key and old key
    
    def shake(self, key):
        #shake key here
        return key
    
    #Modified hill climb subroutine that can be used as a worker thread 
    # - adjust max_trials as needed
    # - set silent to true to mute results output
    # - can be run without a thread
    def hillClimb(self, max_trials = 100000, silent = False, thread_name = "standard"):
        maxScore = float("-inf")
        curr_maxScore = float("-inf")
        best_plain_text = ""
        best_key = None

        key = None #define the initial key

        start_t = time()

        idle = 0
        for trials in range(max_trials):
            key, old_key = self.shuffle(key)

            plain_text = self.decipher(key)

            score = evaluater.evaluate.evaluateQuadgramFrequencies(plain_text)

            if score > maxScore:
                maxScore = score
                curr_maxScore = score
                best_plain_text = plain_text
                best_key = key
                
                if not silent:
                    print("Score:", maxScore)
                    print("Number of Trials:", trials + 1)
                    print(" >", plain_text)
                    print("Key:", key)
                    print()
            elif score > curr_maxScore:
                curr_maxScore = score
            else:
                key = old_key

                idle += 1

                if idle > 1000: #adjust as needed
                    idle = 0
                    key = self.shake(key)

                    curr_maxScore = evaluater.evaluate.evaluateQuadgramFrequencies(plain_text)

        end_t = time()

        if not silent:
            print()
            print("[ RESULTS ]")
            print("-------------------------------------------------------------------------------")
            print("Time elapsed:", end_t - start_t)
            print("Max score achieved:", maxScore)
            print("Trials:", trials + 1)
            print(" >", best_plain_text)
            print("------------------")
            print("Best key:", key)


        self.__trials += trials + 1

        self.__results[thread_name] = {
            "bestscore": maxScore, 
            "bestplaintext": best_plain_text, 
            "bestkey": best_key
        }

    #Threaded hillClimb subroutine
    # - leave max_trials empty for automatic max_trials calculation
    # - thread_names is a placeholder for whatever range/collection of keys that need to be poped onto seperate threads
    def parallel_hillClimb(self, max_trials = -1):
        self.__trials = 0

        thread_names = []

        #calculate max number of trials needed
        if max_trials == -1:
            max_trials = auto_ciel // len(cipher_text) + auto_floor

        print("[ PROGRAM STARTED ]")

        start_t = time()

        for thread_name in thread_names:
            self.__worker_threads.append([Thread(target = self.hillClimb, args = ()), thread_name])
            self.__worker_threads[-1][0].start()
            print(f">>> Thread {thread_name} has started")
        
        print("\nrunning...\n")
        
        for thread_data in self.__worker_threads:
            thread_data[0].join()
            self.__worker_threads.remove(thread_data)
            print(f">>> Thread {thread_data[1]} has ended")
        
        end_t = time()

        print("[ PROGRAM ENDED ]")

        #get best key
        best_score = (0, float("-inf"))
        for thread_name, result in self.__results.items():
            if result["bestscore"] > best_score[1]:
                best_score = (thread_name, result["bestscore"])
        
        best_thread = best_score[0]
        best_result = self.__results[best_thread]

        print()
        print("[ RESULTS ]")
        print("-------------------------------------------------------------------------------")
        print("Time elapsed:", end_t - start_t)
        print("Max score achieved:", best_result["bestscore"])
        print("Total trials:", self.__trials)
        print(" >", best_result["bestplaintext"])
        print("------------------")
        print("Best key:", best_result["bestkey"])
        print("Best thread:", best_thread)

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
    cipher_text = load_ciphertext("inp.txt")
    
    hill_climber = Parallel_HillClimb(cipher_text)

    #Parallel method
    hill_climber.parallel_hillClimb()

