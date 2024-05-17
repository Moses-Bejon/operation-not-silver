#include <string>
#include <fstream>
#include <unordered_map>           

using namespace std;


struct Weight {
    double value;

    Weight(double v) : value(v) {}

    Weight() : value(-25.0) {}
};

double operator+=(double& lhs, const Weight& rhs) {
    lhs += rhs.value;
}

//rewritten evaluate class that uses text file version of quadgram proportions because json requires external module to work 
//(also slightly speedier than json)
//some weird logic was required for the unordered map data structure
class Evaluate {
    private:
        unordered_map<string, Weight> idealQuadgramFrequencies;
        string quadgram;
        double weight;

    public:
        Evaluate() {
            ifstream quadgramFile("evaluater/quadgram proportions.txt");
            while (quadgramFile >> quadgram >> weight) {
                idealQuadgramFrequencies[quadgram] = weight;
            }
            quadgramFile.close();
        }

        double evaluateQuadgramFrequencies(string plaintext) {
            double fitness = 0;
            string window = plaintext.substr(0, 4);

            for (char letter: plaintext.substr(4)) {
                fitness += idealQuadgramFrequencies[window];

                //window[0], window[1], window[2], window[3] = window[1], window[2], window[3], letter;
                window[0] = window[1]; 
                window[1] = window[2];
                window[2] = window[3];
                window[3] = letter;
            }
            return fitness;
        }
}; 



