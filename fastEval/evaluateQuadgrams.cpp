#include <iostream>
#include <cstring>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sstream>

double fitness;
int currentHash;
int first;
int last;

void* open_shared_memory(const std::string& shm_name, size_t size) {
    int fd = shm_open(('/' + shm_name).c_str(), O_RDONLY, 0222); 
    void* addr = mmap(nullptr, size, PROT_READ, MAP_SHARED, fd, 0);
    close(fd);

    return addr;
}

int get_int_from_chars(const char* chars_val) {
    std::stringstream str_val;
    str_val << chars_val;
    int int_val;
    str_val >> int_val;

    return int_val;
}

int calculateHash(int* quadgram) {
    return quadgram[0] * 17576 + quadgram[1] * 676 + quadgram[2] * 26 + quadgram[3];
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
    //get input from python module
    const char* shm_name = argv[1];

    char* plaintext_str;
    int plaintext_len = get_int_from_chars(argv[2]); 
    int plaintext[plaintext_len];

    //connect to shared memory to access ideal quadgram frequencies
    void* shm_addr = open_shared_memory(shm_name, 3655808);

    //type cast shared array pointer to double pointer
    double* idealQuadgramFrequencies = static_cast<double*>(shm_addr);

    while (true) {
        fitness = 0;
        std::cin >> plaintext_str;

        for (size_t i = 0; i < plaintext_len; i++) {
            plaintext[i] = plaintext_str[i] - 97;
        }

        //output to stdout file to be read by python
        std::cout << evaluateQuadgramFrequencies(idealQuadgramFrequencies, plaintext, plaintext_len) << std::endl;   
    }

    //clean up connection
    munmap(shm_addr, 3655808);

    return 0;
}


//compile:
//  c++ -o evaluateQuadgrams evaluateQuadgrams.cpp