//standard modules:
#include <iostream>
#include <string>
#include <cmath>
#include <limits>
#include <fstream>
#include <algorithm>
#include <chrono>

//bespoke modules:
#include "../evaluaterCpp/evaluater.cpp"

using namespace std;


//get deepcopy of 2x2 int array
void deepCopy2dArray(int source[][2], int destination[][2]) {
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            destination[i][j] = source[i][j];
        }
    }
}

static int char_to_int(char character) {
    return int(tolower(character)) - 97;
}

static char int_to_char(int charCode) {
    return char(charCode + 97);
}

//algorithm to calculate determinant of 2x2
static int calc_det(int key_matrix[2][2]) {
    return (key_matrix[0][0] * key_matrix[1][1]) - (key_matrix[0][1] * key_matrix[1][0]);
}

//honestly have no clue what is happening here but it works so...
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
    for (int i = 0; i < 2; i++) {
        moduloMatrixInv[i] = new int[2];
        for (int j = 0; j < 2; j++) {
            int invMember = (adjugate[i][j] * det_inv) % 26;

            // Ensure result is positive or zero
            if (invMember < 0) {
                invMember += 26;  
            }
            moduloMatrixInv[i][j] = invMember;
        }
    }

    return moduloMatrixInv;
}

//decrypt ciphertext using 2x2 int array key
string decipher(string ciphertext, int inv_key[2][2]) {
    string plaintext = "";

    int length = ciphertext.length();
    //apply inverse key to every 2 chunks of the ciphertext
    for (int i = 0; i < length; i += 2) {
        int word[2] = {char_to_int(ciphertext[i]), char_to_int(ciphertext[i + 1])};

        int result[2] = {
            inv_key[0][0] * word[0] + inv_key[0][1] * word[1], 
            inv_key[1][0] * word[0] + inv_key[1][1] * word[1]
        };
        
        //concatenate the result to the end of plaintext
        plaintext += int_to_char(result[0] % 26);
        plaintext += int_to_char(result[1] % 26);
    }

    return plaintext;
}

//special print procedure to produce a status update
void printEncryptionSet(string ciphertext, int inv_key[2][2], double score) {
    string full_plaintext = decipher(ciphertext, inv_key);

    int** key = mod_matrix_inv(inv_key);

    cout << "\n";
    cout << full_plaintext << "\n";
    cout << "Score:" << score << "\n";
    cout << "key:\n";
    cout << key[0][0] << " " << key[0][1] << "\n";
    cout << key[1][0] << " " << key[1][1] << "\n";

    //free up memory to prevent memory leak
    for (int i = 0; i < 2; ++i) {
        delete[] key[i];
    }
    delete[] key;
}

//main brute force procedure
void keyDictAttack(string ciphertext, int testChunk = -1, int notiPer = 500000) {
    int key[2][2];
    int bestKey[2][2];
    double maxScore = - numeric_limits<double>::infinity(); //double negative infinity
    int trials = 0;

    //take a segment of the cyphertext rather than the whole thing 
    string ciphertext_seg; 
    if (testChunk == -1) {
        ciphertext_seg = ciphertext;
    }
    else {
        ciphertext_seg = ciphertext.substr(0, testChunk);
    }

    //remove spaces from ciphertext string
    ciphertext_seg.erase(remove_if(ciphertext_seg.begin(), ciphertext_seg.end(), ::isspace), ciphertext_seg.end());
    ciphertext.erase(remove_if(ciphertext.begin(), ciphertext.end(), ::isspace), ciphertext.end()); 

    //filestream for key dict
    ifstream hillKeyFile("hill_2x2_inv_keys.txt");

    string plaintext;
    Evaluate evaluater;
    double score = 0;

    cout << "[ KEY DICT ATTACK STARTED ]\n";

    //start timer
    __1::chrono::steady_clock::time_point start_t = chrono::steady_clock::now();

    //brute forcer mainloop
    while (hillKeyFile >> key[0][0] >> key[0][1] >> key[1][0] >> key[1][1]) {
        plaintext = decipher(ciphertext_seg, key);

        score = evaluater.evaluateQuadgramFrequencies(plaintext);

        //save and display new best result
        if (score > maxScore) {
            printEncryptionSet(ciphertext, key, score);
            maxScore = score;
            deepCopy2dArray(key, bestKey);
        }

        trials++;
        if (trials % notiPer == 0) {
            cout << ">>> Number of trials ran: " << trials << "\n";
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
    printEncryptionSet(ciphertext, bestKey, maxScore);

    cout << "Total number of trials:" << trials << "\n";

    chrono::duration<double> time_elapsed = end_t - start_t;
    cout << "Time elapsed: " << time_elapsed.count() << "\n";
}


int main() {
    //chapter 10A (2023)
    string ciphertext = "HHIZR KHHXH XCFWL WJHIC YFPAX FHHZD VZLWJ HREXL CGWPP XUWSK EEQTP WDSCA ICHHZ DHVPQ NGAEU CNUAH VQJOV ILWJH VZCEL PLTLD NNNHR RPTQT AHXQE EUCGZ LPRFW QQUGZ WAVOW KGZCQ KKZNY ITMMM ASMQW APRPN IBHKL TRIYY QTTHH UWPLP THWHK GVITG HAWOA WVDGZ HALPJ RQTVI OWZGI CORHH ZDBPB JGKEF JOFWX QLPLT RIFMS KAHWO MYWOB JVXPX TZLEJ UEELE LPHKB UWKBP YRLPU IORVP LQICQ TRVQJ HVLEN APTQI PDBZD KKMZR IMEWA OVZAH NACEW EPRLO REGKA HXQBY BJWAP RPNIB HKVPG THAVI NAUQY WAEHH ZDWAR EFJTH VZVIA HASCC WABUZ GICOR FJAHT IVMJN VOXBL ETHFT LCKBI QRVWO EABOL DYWNA KWFWV MOUAT BPXYN GAERR FXAMX QWOLD BOAHG IXMLP KDBYT TQTSK AELTU WMEWA LTEMW HVZPT SKEEJ NLAFT BQLDH VLPAP AHQCB OAHFG GYXCF WGSBU PXXHM ABIVQ EECTE EBZMG MSWOX BDDUW LPXRP TGUEA TEEXP NHVLE KMDWH AHHUV NGNSA EKOTT LJMGB UBCJH TKNCB JJQVI LDWNA MAHJO SKXBK DRRVI IMSSL ELPAC RRMWB UUGOU ATJDM XASZR AMSGY RVJWA HVVCV QCAIC UITTA HSGPN BCICP LHHPL SKUIV IUIVD HHDDM GHWKM WKYJS KPLIM LMNGP WDGGZ NNTEH KLWEX LPHLT TTESS QTAHV MAWVM WOBJW HFKAW MGGVZ HWAAI GZLPA LIQGZ BYBJK YQTVM VJIUN AMAYR LPVZT KCKLD HHDDC TEEBZ KYBLH KBUIC FRYWF JAHCA EMWHK OBJGZ ICJQH VXBWH MEEAT EAPVW TBZGA HGIXM LPRRQ TOSZA JOFWA WAWRR JDHZS WZDPN BOWOV JFQEF EEMXX QGYIM VJEMP LFWCU ZUREN SAHCA CCGZS JEESA HVGZL PZQKG GZLPQ IVJFQ KRVQI MBPAG ATUAC QOPRK LPRER FYRLP BYVMK SWANA RFHJI CJBMU EMWHJ DMXAS ATLPH LTKNC TTMGM GLWVI AHQCE EGZUG LSVQE EXOEE AHZKL OYWAH CAXKK GVJPI RUWEI XFTTX CNGOG ZLPME AHICN UPWDS CAICT BOSKS ANMYB OYFRU MUDON AJPXQ SSZNH VXPBP OGVCV MWOVJ XFTZT HRRDK BUGIY PASFR SKZNY IVILQ FWWWU XHVWA MUTZM AUUUV PTVXS DCAVI AHWOG XVIPY RUMQ";
    keyDictAttack(ciphertext, 23); //feeding 0-20 part of the chyphertext

    //string ciphertext = "avdxislqsbriuaanrhklthxcienagspxxckmqityaxejisgg";
    //string ciphertext = "vuqxyugfyzfjgoccjkxlqvguczymjhpmjkyzoilsxlwtmccclwizqbetwthkkvilkruufwuu";

    return 0;
}