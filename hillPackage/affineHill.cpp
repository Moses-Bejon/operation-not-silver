//standard modules:
#include <iostream>
#include <string>
#include <limits>
#include <fstream>
#include <chrono>

//bespoke modules:
#include "evaluater/evaluater.cpp"

using namespace std;


//get deepcopy of 2x2 int array
void deepCopy2dArray(int source[][2], int destination[][2]) {
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            destination[i][j] = source[i][j];
        }
    }
}

static char int_to_char(int charCode) {
    return char(charCode + 97);
}

void printIntStr(int* intStr, int len) {
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
int** mod_matrix_inv(int matrix[2][2]) {
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

//decrypt ciphertext using 2x2 int array key
int* decipher(int* ciphertext, int len, int inv_key[2][2], int a, int b) {
    int left_val;
    int right_val;

    int* plaintext = new int[len];

    //apply decryption to every 2 chunks of the ciphertext
    for (int i = 0; i < len; i += 2) {
        //undo a,b vector offset
        left_val = (ciphertext[i] - a + 26) % 26;
        right_val = (ciphertext[i + 1] - b + 26) % 26;

        //apply inverse key matrix and add to plaintext
        plaintext[i] = (inv_key[0][0] * left_val + inv_key[0][1] * right_val) % 26;
        plaintext[i + 1] = (inv_key[1][0] * left_val + inv_key[1][1] * right_val) % 26;
    }

    return plaintext;
}

//special print procedure to produce a status update
void printEncryptionSet(int* ciphertext, int len, int inv_key[2][2], int a, int b, double score) {
    int* full_plaintext = decipher(ciphertext, len, inv_key, a, b);

    int** key = mod_matrix_inv(inv_key);

    cout << "\n";
    printIntStr(full_plaintext, len);
    cout << "Score:" << score << "\n";
    cout << "key:\n";
    cout << key[0][0] << " " << key[0][1] << "\n";
    cout << key[1][0] << " " << key[1][1] << "\n";
    cout << "offset:\n";
    cout << a << " " << b << "\n";

    //free up memory to prevent memory leak
    for (int i = 0; i < 2; i++) {
        delete[] key[i];
    }
    delete[] key;

    delete[] full_plaintext;
}

//main brute force procedure
void keyDictAttack(int* ciphertext, int subLen, int len, int notiPer = 1000000) {
    int key[2][2];
    int bestKey[2][2];
    double maxScore = - numeric_limits<double>::infinity(); //double negative infinity
    int trials = 0;

    //filestream for key dict
    ifstream hillKeyFile("hill_2x2_inv_keys.txt");

    Evaluate evaluater;
    double score = 0;

    cout << "[ KEY DICT ATTACK STARTED ]\n";

    //start timer
    __1::chrono::steady_clock::time_point start_t = chrono::steady_clock::now();

    int best_a = 0;
    int best_b = 0;

    //brute forcer mainloop
    while (hillKeyFile >> key[0][0] >> key[0][1] >> key[1][0] >> key[1][1]) {
        for (int a = 0; a < 26; a++) {
            for (int b = 0; b < 26; b++) {
                int* plaintext = decipher(ciphertext, subLen, key, a, b);

                score = evaluater.evaluateQuadgramFrequencies(plaintext, subLen);

                //save and display new best result
                if (score > maxScore) {
                    printEncryptionSet(ciphertext, len, key, a, b, score);
                    maxScore = score;
                    deepCopy2dArray(key, bestKey);
                    best_a = a;
                    best_b = b;
                }

                trials++;
                
                if (trials % notiPer == 0) {
                    cout << ">>> Number of trials ran: " << trials << "\n";
                }

                //to prevent memory leak
                delete[] plaintext;
            }
        }
    }

    //end timer
    __1::chrono::steady_clock::time_point end_t = chrono::steady_clock::now();

    cout << "[ KEY DICT ATTACK ENDED ]\n";

    hillKeyFile.close();


    //display results:
    cout << "\n---------------------------------------------------------------------------------------------------------------------------------------\n";
    cout << "[ STATUS ] \n";
    cout << ">>> Best result:";
    printEncryptionSet(ciphertext, len, bestKey, best_a, best_b, maxScore);

    cout << "Total number of trials:" << trials << "\n";

    chrono::duration<double> time_elapsed = end_t - start_t;
    cout << "Time elapsed: " << time_elapsed.count() << "\n";
}


int main() {
    //chapter 10A (2023)
    string ciphertext_str = "HHIZR KHHXH XCFWL WJHIC YFPAX FHHZD VZLWJ HREXL CGWPP XUWSK EEQTP WDSCA ICHHZ DHVPQ NGAEU CNUAH VQJOV ILWJH VZCEL PLTLD NNNHR RPTQT AHXQE EUCGZ LPRFW QQUGZ WAVOW KGZCQ KKZNY ITMMM ASMQW APRPN IBHKL TRIYY QTTHH UWPLP THWHK GVITG HAWOA WVDGZ HALPJ RQTVI OWZGI CORHH ZDBPB JGKEF JOFWX QLPLT RIFMS KAHWO MYWOB JVXPX TZLEJ UEELE LPHKB UWKBP YRLPU IORVP LQICQ TRVQJ HVLEN APTQI PDBZD KKMZR IMEWA OVZAH NACEW EPRLO REGKA HXQBY BJWAP RPNIB HKVPG THAVI NAUQY WAEHH ZDWAR EFJTH VZVIA HASCC WABUZ GICOR FJAHT IVMJN VOXBL ETHFT LCKBI QRVWO EABOL DYWNA KWFWV MOUAT BPXYN GAERR FXAMX QWOLD BOAHG IXMLP KDBYT TQTSK AELTU WMEWA LTEMW HVZPT SKEEJ NLAFT BQLDH VLPAP AHQCB OAHFG GYXCF WGSBU PXXHM ABIVQ EECTE EBZMG MSWOX BDDUW LPXRP TGUEA TEEXP NHVLE KMDWH AHHUV NGNSA EKOTT LJMGB UBCJH TKNCB JJQVI LDWNA MAHJO SKXBK DRRVI IMSSL ELPAC RRMWB UUGOU ATJDM XASZR AMSGY RVJWA HVVCV QCAIC UITTA HSGPN BCICP LHHPL SKUIV IUIVD HHDDM GHWKM WKYJS KPLIM LMNGP WDGGZ NNTEH KLWEX LPHLT TTESS QTAHV MAWVM WOBJW HFKAW MGGVZ HWAAI GZLPA LIQGZ BYBJK YQTVM VJIUN AMAYR LPVZT KCKLD HHDDC TEEBZ KYBLH KBUIC FRYWF JAHCA EMWHK OBJGZ ICJQH VXBWH MEEAT EAPVW TBZGA HGIXM LPRRQ TOSZA JOFWA WAWRR JDHZS WZDPN BOWOV JFQEF EEMXX QGYIM VJEMP LFWCU ZUREN SAHCA CCGZS JEESA HVGZL PZQKG GZLPQ IVJFQ KRVQI MBPAG ATUAC QOPRK LPRER FYRLP BYVMK SWANA RFHJI CJBMU EMWHJ DMXAS ATLPH LTKNC TTMGM GLWVI AHQCE EGZUG LSVQE EXOEE AHZKL OYWAH CAXKK GVJPI RUWEI XFTTX CNGOG ZLPME AHICN UPWDS CAICT BOSKS ANMYB OYFRU MUDON AJPXQ SSZNH VXPBP OGVCV MWOVJ XFTZT HRRDK BUGIY PASFR SKZNY IVILQ FWWWU XHVWA MUTZM AUUUV PTVXS DCAVI AHWOG XVIPY RUMQ";
    
    //remove spaces from ciphertext string
    ciphertext_str.erase(remove_if(ciphertext_str.begin(), ciphertext_str.end(), ::isspace), ciphertext_str.end()); 

    int len = ciphertext_str.length();

    int ciphertext[len];
    for (int i = 0; i < len; i++) {
        ciphertext[i] = tolower(ciphertext_str[i]) - 97;
    }

    int testChunk = 18; //feeding only part of the chyphertext
    keyDictAttack(ciphertext, testChunk, len); 

    return 0;
}