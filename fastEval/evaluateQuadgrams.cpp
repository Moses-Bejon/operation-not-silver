#include <iostream>
#include <sstream>
#include <fstream>
#include <string.h>

double fitness;
int currentHash;
int first;
int last;
double idealQuadgramFrequencies[456976];
std::string quadgram;
double weight;

int calculateHash(int* quadgram) {
    return quadgram[0] * 17576 + quadgram[1] * 676 + quadgram[2] * 26 + quadgram[3];
}

int calculateHash(std::string quadgram) {
    return (quadgram[0] - 97) * 17576 + (quadgram[1] - 97) * 676 + (quadgram[2] - 97) * 26 + (quadgram[3] - 97);
}

void load_idealFreqs() {
    for (int i = 0; i < 456976; i++) {
        idealQuadgramFrequencies[i] = -25.0;
    }
    //std::cout << "hi" << std::endl;

    std::ifstream quadgramFile("./quadgram proportions.txt");
    while (quadgramFile >> quadgram >> weight) {
        idealQuadgramFrequencies[calculateHash(quadgram)] = weight;
    }
    quadgramFile.close();
}

int get_int_from_chars(const char* chars_val) {
    std::stringstream str_val;
    str_val << chars_val;
    int int_val;
    str_val >> int_val;

    return int_val;
}

double evaluateQuadgramFrequencies(double* idealQuadgramFrequencies, int* plaintext, int plaintext_len) {
    currentHash = calculateHash(plaintext);
    
    for (int i = 0; i < plaintext_len - 4; i++) {
        first = plaintext[i] * 17576;
        last = plaintext[i + 4];

        fitness += idealQuadgramFrequencies[currentHash];

        currentHash = 26 * (currentHash - first) + last;
    }

    return fitness;
}

int main(int argc, char* argv[]) {
    std::string plaintext_str;
    int plaintext_len = get_int_from_chars(argv[1]); 
    int plaintext[plaintext_len];

    load_idealFreqs();

    while (true) {
        fitness = 0;
        std::cin >> plaintext_str;

        for (size_t i = 0; i < plaintext_len; i++) {
            plaintext[i] = plaintext_str[i] - 97;
        }

        //output to stdout file to be read by python
        std::cout << evaluateQuadgramFrequencies(idealQuadgramFrequencies, plaintext, plaintext_len) << '\n';   
    }

    return 0;
}


//compile:
//  c++ -o evaluateQuadgrams evaluateQuadgrams.cpp