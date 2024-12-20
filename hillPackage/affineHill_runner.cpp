#include <iostream>
#include "./threadAffineHill.cpp"

using namespace std;

int main() {
    //chapter 10A (2023)
    string ciphertext_str = "HHIZR KHHXH XCFWL WJHIC YFPAX FHHZD VZLWJ HREXL CGWPP XUWSK EEQTP WDSCA ICHHZ DHVPQ NGAEU CNUAH VQJOV ILWJH VZCEL PLTLD NNNHR RPTQT AHXQE EUCGZ LPRFW QQUGZ WAVOW KGZCQ KKZNY ITMMM ASMQW APRPN IBHKL TRIYY QTTHH UWPLP THWHK GVITG HAWOA WVDGZ HALPJ RQTVI OWZGI CORHH ZDBPB JGKEF JOFWX QLPLT RIFMS KAHWO MYWOB JVXPX TZLEJ UEELE LPHKB UWKBP YRLPU IORVP LQICQ TRVQJ HVLEN APTQI PDBZD KKMZR IMEWA OVZAH NACEW EPRLO REGKA HXQBY BJWAP RPNIB HKVPG THAVI NAUQY WAEHH ZDWAR EFJTH VZVIA HASCC WABUZ GICOR FJAHT IVMJN VOXBL ETHFT LCKBI QRVWO EABOL DYWNA KWFWV MOUAT BPXYN GAERR FXAMX QWOLD BOAHG IXMLP KDBYT TQTSK AELTU WMEWA LTEMW HVZPT SKEEJ NLAFT BQLDH VLPAP AHQCB OAHFG GYXCF WGSBU PXXHM ABIVQ EECTE EBZMG MSWOX BDDUW LPXRP TGUEA TEEXP NHVLE KMDWH AHHUV NGNSA EKOTT LJMGB UBCJH TKNCB JJQVI LDWNA MAHJO SKXBK DRRVI IMSSL ELPAC RRMWB UUGOU ATJDM XASZR AMSGY RVJWA HVVCV QCAIC UITTA HSGPN BCICP LHHPL SKUIV IUIVD HHDDM GHWKM WKYJS KPLIM LMNGP WDGGZ NNTEH KLWEX LPHLT TTESS QTAHV MAWVM WOBJW HFKAW MGGVZ HWAAI GZLPA LIQGZ BYBJK YQTVM VJIUN AMAYR LPVZT KCKLD HHDDC TEEBZ KYBLH KBUIC FRYWF JAHCA EMWHK OBJGZ ICJQH VXBWH MEEAT EAPVW TBZGA HGIXM LPRRQ TOSZA JOFWA WAWRR JDHZS WZDPN BOWOV JFQEF EEMXX QGYIM VJEMP LFWCU ZUREN SAHCA CCGZS JEESA HVGZL PZQKG GZLPQ IVJFQ KRVQI MBPAG ATUAC QOPRK LPRER FYRLP BYVMK SWANA RFHJI CJBMU EMWHJ DMXAS ATLPH LTKNC TTMGM GLWVI AHQCE EGZUG LSVQE EXOEE AHZKL OYWAH CAXKK GVJPI RUWEI XFTTX CNGOG ZLPME AHICN UPWDS CAICT BOSKS ANMYB OYFRU MUDON AJPXQ SSZNH VXPBP OGVCV MWOVJ XFTZT HRRDK BUGIY PASFR SKZNY IVILQ FWWWU XHVWA MUTZM AUUUV PTVXS DCAVI AHWOG XVIPY RUMQ";
    
    //string ciphertext_str = "mdrntrobtgajgwzdxzrrzrohlqnsdrvkgwmrgwczlfvqamjbbolwyhqxhwzddfrwshmnhyfyiqw";

    //remove spaces from ciphertext string
    ciphertext_str.erase(remove_if(ciphertext_str.begin(), ciphertext_str.end(), ::isspace), ciphertext_str.end()); 

    int len = ciphertext_str.length();

    int ciphertext[len];
    for (int i = 0; i < len; i++) {
        ciphertext[i] = tolower(ciphertext_str[i]) - 97;
    }

    //18-22 recomended for quadgrams
    //33-40 recomended for bigrams
    int testChunk = 18; //feeding only part of the chyphertext

    AffineHill cipherEngine(ciphertext, len);

    //Fastest mode for m1 macbook air
    cipherEngine.keyDictAttack(testChunk, 4, 0, true); 

    //Debugging mode for m1 macbook air
    //cipherEngine.keyDictAttack(testChunk, 3); 

    return 0;
}

//Full terminal commands for whtn thread module not compiling properly:
//  Compile:
//      g++ -std=c++17 -o affineHill_runner affineHill_runner.cpp
//  Execute:
//      ./affineHill_runner