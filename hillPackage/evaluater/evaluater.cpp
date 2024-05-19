#include <string>
#include <fstream>       

using namespace std;


class Evaluate {
    private:
        double idealQuadgramFrequencies[456976];
        string quadgram;
        double weight;

    public:
        Evaluate() {
            for (int i = 0; i < 456976; i++) {
                idealQuadgramFrequencies[i] = -25.0;
            }

            ifstream quadgramFile("../evaluater/quadgram proportions.txt");
            while (quadgramFile >> quadgram >> weight) {
                idealQuadgramFrequencies[calculateHash(quadgram)] = weight;
            }
            quadgramFile.close();
        }

        double evaluateQuadgramFrequencies(int* plaintext, int plaintext_len) {
            double fitness = 0;
            int currentHash = calculateHash(plaintext);
            int first;
            int last;

            for (int i = 0; i < plaintext_len - 4; i++) {
                first = plaintext[i] * 17576;
                last = plaintext[i + 4];

                fitness += idealQuadgramFrequencies[currentHash];

                currentHash = 26 * (currentHash - first) + last;
            }

            return fitness;
        }

        int calculateHash(int* quadgram) {
            return quadgram[0] * 17576 + quadgram[1] * 676 + quadgram[2] * 26 + quadgram[3];
        }

        int calculateHash(string quadgram) {
            return (quadgram[0] - 97) * 17576 + (quadgram[1] - 97) * 676 + (quadgram[2] - 97) * 26 + (quadgram[3] - 97);
        }
}; 

