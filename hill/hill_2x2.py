import numpy as np
import evaluate

def char_to_int(char: str):
    #Assumes that char isalpha
    return ord(char.lower()) - 97

def int_to_char(charCode: int):
    #Assumes that charCode is for a lower alpha char starting with 0 as "a" and 25 as "z"
    return chr(charCode + 97)

def calc_det(matrix) -> int:
    determinant = np.linalg.det(matrix)
    intDet = int(np.round(determinant))

    return intDet

#Some linear algebra magic that gets the modulo inverse of the key matrix (I honestly have no idea why this works)
def mod_matrix_inv(matrix):
    #Calculate determinant and round to int
    intDet = calc_det(matrix)

    #Calculate the modulo inverse of the determinant
    det_inv = pow(intDet, -1, 26)

    #Calculate adjugate and round to int
    matrixInv = np.linalg.inv(matrix)
    adjugate = np.round(intDet * matrixInv).astype(int)

    #Multiply by inverse determinant and apply modulus
    moduloMatrixInv = (adjugate * det_inv) % 26        

    return moduloMatrixInv

def decipher(cipher, key):
        #Note that the decypher method always assumes that the key is invertable

        n = len(key)
        cipher_text = cipher.lower().replace(" ", "")
        plain_text = ""

        #padding to avoid matrix size issues with cyphertext (padding with a because I'm lazy)
        amountOfPadding = (n - len(cipher_text) % n) % n
        cipher_text += "a" * amountOfPadding

        key = np.array(key)
        key_inverse = mod_matrix_inv(key)
        

        #Iterates over n sized chunks of cyphertext to decode, I'll call each chunk a "word" because that sounds cool and no-one can stop me. (BTW, hi Moses!)
        for i in range(0, len(cipher_text), n):
            #Turning each word into an n sized matrix
            word = [char_to_int(char) for char in cipher_text[i : i + n]]
            word = np.array(word)
            word = word.reshape((n, 1))

            #Getting plaintext from dot product and then mod 26
            result = np.dot(key_inverse, word)

            #converting each character in row into characters
            for char in result:
                charCode = int(round(char[0])) #annoying numpy floating point fix
                plain_text += int_to_char(charCode % 26)

        return plain_text

key = [[0, 0], [0, 0]]
cipher_text = "HHIZR KHHXH XCFWL WJHIC YFPAX FHHZD VZLWJ HREXL CGWPP XUWSK EEQTP WDSCA ICHHZ DHVPQ NGAEU CNUAH VQJOV ILWJH VZCEL PLTLD NNNHR RPTQT AHXQE EUCGZ LPRFW QQUGZ WAVOW KGZCQ KKZNY ITMMM ASMQW APRPN IBHKL TRIYY QTTHH UWPLP THWHK GVITG HAWOA WVDGZ HALPJ RQTVI OWZGI CORHH ZDBPB JGKEF JOFWX QLPLT RIFMS KAHWO MYWOB JVXPX TZLEJ UEELE LPHKB UWKBP YRLPU IORVP LQICQ TRVQJ HVLEN APTQI PDBZD KKMZR IMEWA OVZAH NACEW EPRLO REGKA HXQBY BJWAP RPNIB HKVPG THAVI NAUQY WAEHH ZDWAR EFJTH VZVIA HASCC WABUZ GICOR FJAHT IVMJN VOXBL ETHFT LCKBI QRVWO EABOL DYWNA KWFWV MOUAT BPXYN GAERR FXAMX QWOLD BOAHG IXMLP KDBYT TQTSK AELTU WMEWA LTEMW HVZPT SKEEJ NLAFT BQLDH VLPAP AHQCB OAHFG GYXCF WGSBU PXXHM ABIVQ EECTE EBZMG MSWOX BDDUW LPXRP TGUEA TEEXP NHVLE KMDWH AHHUV NGNSA EKOTT LJMGB UBCJH TKNCB JJQVI LDWNA MAHJO SKXBK DRRVI IMSSL ELPAC RRMWB UUGOU ATJDM XASZR AMSGY RVJWA HVVCV QCAIC UITTA HSGPN BCICP LHHPL SKUIV IUIVD HHDDM GHWKM WKYJS KPLIM LMNGP WDGGZ NNTEH KLWEX LPHLT TTESS QTAHV MAWVM WOBJW HFKAW MGGVZ HWAAI GZLPA LIQGZ BYBJK YQTVM VJIUN AMAYR LPVZT KCKLD HHDDC TEEBZ KYBLH KBUIC FRYWF JAHCA EMWHK OBJGZ ICJQH VXBWH MEEAT EAPVW TBZGA HGIXM LPRRQ TOSZA JOFWA WAWRR JDHZS WZDPN BOWOV JFQEF EEMXX QGYIM VJEMP LFWCU ZUREN SAHCA CCGZS JEESA HVGZL PZQKG GZLPQ IVJFQ KRVQI MBPAG ATUAC QOPRK LPRER FYRLP BYVMK SWANA RFHJI CJBMU EMWHJ DMXAS ATLPH LTKNC TTMGM GLWVI AHQCE EGZUG LSVQE EXOEE AHZKL OYWAH CAXKK GVJPI RUWEI XFTTX CNGOG ZLPME AHICN UPWDS CAICT BOSKS ANMYB OYFRU MUDON AJPXQ SSZNH VXPBP OGVCV MWOVJ XFTZT HRRDK BUGIY PASFR SKZNY IVILQ FWWWU XHVWA MUTZM AUUUV PTVXS DCAVI AHWOG XVIPY RUMQ"
maxScore = float("-inf")
trials = 0

print("[ STARTED ]")
with open("hill_2x2_keys.txt", "r") as f:
    hasKey = True
    while hasKey:
        line = f.readline().strip()
        if line != "":
            line_list = line.split(" ")
            key[0][0], key[0][1], key[1][0], key[1][1]  = int(line_list[0]), int(line_list[1]), int(line_list[2]), int(line_list[3])

            plaintext = decipher(cipher_text, key)

            score = evaluate.evaluateQuadgramFrequencies(plaintext)

            if score > maxScore:
                maxScore = score
                print("")
                print(plaintext)
                print(score)
                print(key)


            trials += 1
            if trials % 5000 == 0:
                print(">>> Number of trials completed:", trials)
                print(">>> Current max score:", maxScore)
        else:
            hasKey = False

print("[ ENDED ]")
