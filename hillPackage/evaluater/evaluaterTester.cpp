#include <chrono>
#include <iostream>
#include <fstream>

//bespoke modules:
#include "../evaluater/evaluater.cpp"

using namespace std;



int main() {
    int n = 10000;
    double score;
    Evaluate evaluater;
    
    string plaintext;
    ifstream hillKeyFile("../evaluater/fast.txt");

    getline(hillKeyFile, plaintext);

    double total_time_elapsed = 0;
    for (int i = 0; i < n; i++) {
        cout << "[ STARTED ]" << endl;
        __1::chrono::steady_clock::time_point start_t = chrono::steady_clock::now();

        score = evaluater.evaluateQuadgramFrequencies(plaintext);

        __1::chrono::steady_clock::time_point end_t = chrono::steady_clock::now();
        cout << "[ ENDED ]" << endl;

        cout << "Score: " << score << endl;

        chrono::duration<double> time_elapsed = end_t - start_t;
        total_time_elapsed += time_elapsed.count();
    }

    cout << "Time elapsed: " << total_time_elapsed / n << endl;

    return 0;
}