#include <chrono>
#include <iostream>
#include <fstream>

//bespoke modules:
#include "../evaluater/evaluater.cpp"

using namespace std;


int main() {
    int n = 10;
    double score;
    Evaluate evaluater;
    
    string plaintext_str;
    ifstream hillKeyFile("../evaluater/fast.txt");

    getline(hillKeyFile, plaintext_str);

    int len = plaintext_str.length();

    int plaintext[len];

    for (int i = 0; i < len; i++) {
        plaintext[i] = plaintext_str[i] - 97;
    }

    double total_time_elapsed = 0;
    for (int i = 0; i < n; i++) {
        cout << "[ STARTED ]\n";
        __1::chrono::steady_clock::time_point start_t = chrono::steady_clock::now();

        score = evaluater.evaluateQuadgramFrequencies(plaintext, len);

        __1::chrono::steady_clock::time_point end_t = chrono::steady_clock::now();
        cout << "[ ENDED ]\n";

        cout << "Score: " << score << "\n";

        chrono::duration<double> time_elapsed = end_t - start_t;
        total_time_elapsed += time_elapsed.count();
    }

    cout << "Time elapsed: " << total_time_elapsed / n << "\n";

    return 0;
}