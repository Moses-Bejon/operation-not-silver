//standard modules:
#include <iostream>
#include <limits>
#include <fstream>
#include <chrono>
#include <thread>
#include <vector>
#include <atomic>

//bespoke modules:
#include "./evaluater/evaluater.cpp"

using namespace std;

const int noOfkeys = 126942;

//get deepcopy of 2x2 int array
static void deepCopy2dArray(int source[][2], int destination[][2]) {
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            destination[i][j] = source[i][j];
        }
    }
}

static int fastModulo26(int x) {
    //return x - (x / 26) * 26;
    int r = x % 26;
    return r + 26 * (r >> 31);
}

static char int_to_char(int charCode) {
    return char(charCode + 97);
}

static void printIntStr(int* intStr, int len) {
    for (int i = 0; i < len; i++) {
        cout << int_to_char(intStr[i]); 
    }
    cout << "\n";
}

//algorithm to calculate determinant of 2x2
static int calc_det(int key_matrix[2][2]) {
    return (key_matrix[0][0] * key_matrix[1][1]) - (key_matrix[0][1] * key_matrix[1][0]);
}

//honestly have no clue what is happening here 
//get the modulo inverse determinant
static int mod_inverse(int det, int m) {
    det = (det % m + m) % m;

    for (int i = 1; i < m; i++) {
        if ((det * i) % m == 1) {
            return i;
        }
    }

    return -1; //mod cannot be found
}

//get the modulo 26 inverse of a matrix (returns 2d pointer)
static int** mod_matrix_inv(int matrix[2][2]) {
    int det = calc_det(matrix);
    int det_inv = mod_inverse(det, 26);

    //calculate adjugate
    int adjugate[2][2] = {
        {matrix[1][1], -matrix[0][1]},
        {-matrix[1][0], matrix[0][0]}
    };

    //invert each member of the matrix individually using inverse determinant
    int** moduloMatrixInv = new int*[2];
    //int invMember;
    for (int i = 0; i < 2; i++) {
        moduloMatrixInv[i] = new int[2];
        for (int j = 0; j < 2; j++) {
            moduloMatrixInv[i][j] = ((adjugate[i][j] * det_inv) % 26 + 26) % 26;
        }
    }

    return moduloMatrixInv;
}

struct keySet {
    double score = -numeric_limits<double>::infinity();
    int key_ref;
};


class Hill {
    public:
        Hill(int* inp_ciphertext, int len) : ciphertext_len(len) {
            ciphertext = new int[ciphertext_len];
            for (int i = 0; i < ciphertext_len; i++) {
                ciphertext[i] = inp_ciphertext[i];
            }

            loadKeys();
        }

        ~Hill() {
            delete[] ciphertext;
        }

        //main brute force procedure
        void keyDictAttack(int test_chunk, int processThreadCount = 1, double notiPer = 200000, bool maxSpeed = false) {
            testChunk = test_chunk;
            atomic<int> trials(0);

            cout << "[ KEY DICT ATTACK STARTED ]\n";

            if (!maxSpeed) {
                //start print thread
                print_thread = thread([this, notiPer] {
                    this->printThread(notiPer);
                });
            }

            //start timer
            start_t = chrono::steady_clock::now();

            // start process threads
            int chunkSize = noOfkeys / processThreadCount;
            for (int i = 0; i < processThreadCount - 1; i++) {
                processThreads.push_back(
                    thread([this, i, chunkSize] {
                        this->processThread(i * chunkSize, chunkSize);
                    })
                );
                cout << ">>> Process thread: " << i << " for keys " << i * chunkSize << " to " << (i + 1) * chunkSize - 1 << " has started\n"; 
            }
            int start = (processThreadCount - 1) * chunkSize;
            processThreads.push_back(
                thread([this, start] {
                    this->processThread(start, noOfkeys - start);
                })
            );
            cout << ">>> Process thread: " << processThreadCount - 1 << " for keys " << start << " to " << noOfkeys - 1 << " has started\n"; 

            //wait for threads to terminate
            for (thread& procThread: processThreads) {
                procThread.join();
            }

            keySet best_key_set;
            for (keySet key_set: processThreadBestKeySets) {
                if (key_set.score > best_key_set.score) {
                    best_key_set = key_set;
                }
            }

            //end timer
            end_t = chrono::steady_clock::now();

            if (!maxSpeed) {
                print_thread.join();
            }

            cout << "[ KEY DICT ATTACK ENDED ]\n";

            //display results:
            cout << "\n---------------------------------------------------------------------------------------------------------------------------------------\n";
            cout << "[ STATUS ] \n";
            cout << ">>> Best result:";

            printEncryptionSet(best_key_set);

            cout << "Total number of trials: " << trials.load() << "\n";

            time_elapsed = end_t - start_t;
            cout << "Time elapsed: " << time_elapsed.count() << "\n";
        }

    private:
        int testChunk;

        int* ciphertext;
        int ciphertext_len;
        int keys[noOfkeys][2][2];
        atomic<int> trials;

        bool globalDataFrozen = false;

        vector<thread> processThreads;
        thread print_thread;
        vector<keySet> processThreadBestKeySets;

        EvaluateQuadgrams evaluater;
        //EvaluateBigrams evaluater;

        //timing attributes
        chrono::steady_clock::time_point start_t;
        chrono::steady_clock::time_point end_t;
        chrono::duration<double> time_elapsed;

        //decrypt ciphertext using 2x2 int array key
        int* decipher(int len, int inv_key[2][2]) {
            int left_val;
            int right_val;

            int* plaintext = new int[len];

            //apply decryption to every 2 chunks of the ciphertext
            for (int i = 0; i < len; i += 2) {
                left_val = ciphertext[i];
                right_val = ciphertext[i + 1];

                //apply inverse key matrix and add to plaintext
                plaintext[i] = (inv_key[0][0] * left_val + inv_key[0][1] * right_val) % 26;
                plaintext[i + 1] = (inv_key[1][0] * left_val + inv_key[1][1] * right_val) % 26;
            }

            return plaintext;
        }

        //special print procedure to produce a status update
        void printEncryptionSet(keySet key_set) {
            int* full_plaintext = decipher(ciphertext_len, keys[key_set.key_ref]);

            int** key = mod_matrix_inv(keys[key_set.key_ref]);

            cout << "\n";
            printIntStr(full_plaintext, ciphertext_len);
            cout << "Score:" << key_set.score << "\n";
            cout << "key:\n";
            cout << key[0][0] << " " << key[0][1] << "\n";
            cout << key[1][0] << " " << key[1][1] << "\n";

            //free up memory to prevent memory leak
            for (int i = 0; i < 2; i++) {
                delete[] key[i];
            }
            delete[] key;

            delete[] full_plaintext;
        }

        void printThread(double notiPer) {
            chrono::steady_clock::time_point timestamp = start_t;
            chrono::steady_clock::time_point current_t;

            while (trials.load() < noOfkeys) {
                current_t = chrono::steady_clock::now();
                if ((current_t - timestamp).count() > notiPer) {
                    cout << ">>> Number of trials ran: " << trials.load() << "\n";
                    timestamp = current_t;
                }
            }
        }

        void loadKeys() {
            //filestream for key dict
            ifstream hillKeyFile("hill_2x2_inv_keys.txt");

            int i = 0;
            while (hillKeyFile >> keys[i][0][0] >> keys[i][0][1] >> keys[i][1][0] >> keys[i][1][1]) {
                i++;
            }
            hillKeyFile.close();
        }

        void processThread(int start, int subLen) {
            double score;

            keySet local_bestData;

            //brute force process mainloop
            for (int i = start; i < start + subLen; i++) {
                int* plaintext = decipher(testChunk, keys[i]);

                score = evaluater.evaluateFrequencies(plaintext, testChunk);

                //save and display new best result
                if (score > local_bestData.score) {
                    local_bestData.score = score;
                    local_bestData.key_ref = i;
                }

                //to prevent memory leak
                delete[] plaintext;

                trials.fetch_add(1);
            }
            processThreadBestKeySets.push_back(local_bestData);
        }
};