import numpy as np
import evaluate

class hill(): # also name the file the same way please
    def __init__(self, cipher):
        self.__cipher: str = cipher #The cipherText
    
    @staticmethod
    def __char_to_int(char: str):
        #Assumes that char isalpha
        return ord(char.lower()) - 97
    
    @staticmethod
    def __int_to_char(charCode: int):
        #Assumes that charCode is for a lower alpha char starting with 0 as "a" and 25 as "z"
        return chr(charCode + 97)
    
    @staticmethod
    def __calc_det(matrix) -> int:
        determinant = np.linalg.det(matrix)
        intDet = int(np.round(determinant))

        return intDet

    #Some linear algebra magic that gets the modulo inverse of the key matrix (I honestly have no idea why this works)
    def __mod_matrix_inv(self, matrix):
        #Calculate determinant and round to int
        intDet = self.__calc_det(matrix)

        #Calculate the modulo inverse of the determinant
        det_inv = pow(intDet, -1, 26)

        #Calculate adjugate and round to int
        matrixInv = np.linalg.inv(matrix)
        adjugate = np.round(intDet * matrixInv).astype(int)

        #Multiply by inverse determinant and apply modulus
        moduloMatrixInv = (adjugate * det_inv) % 26        

        return moduloMatrixInv

    #check if key (matrix) is non-zero and det is coprime to 26
    def is_valid_key(self, key):
        determinant = self.__calc_det(key) % 26
        return determinant != 0 and np.gcd(determinant, 26) == 1

    def decipher(self, cipher_text, key):
        #Note that the decypher method always assumes that the key is invertable and that the cyphertext is the correct size
        #key should be a np array

        n = len(key)
        cipher_text = cipher_text.lower().replace(" ", "")
        plain_text = ""

        key_inverse = self.__mod_matrix_inv(key)
        

        #Iterates over n sized chunks of cyphertext to decode, I'll call each chunk a "word" because that sounds cool and no-one can stop me. 
        for i in range(0, len(cipher_text), n):
            #Turning each word into an n sized matrix
            word = [self.__char_to_int(char) for char in cipher_text[i : i + n]]
            word = np.array(word)
            word = word.reshape((n, 1))

            #Getting plaintext from dot product and then mod 26
            result = np.dot(key_inverse, word)

            #converting each character in row into characters
            for char in result:
                charCode = int(round(char[0])) #annoying numpy floating point fix
                plain_text += self.__int_to_char(charCode % 26)

        return plain_text


    def plainTexts(self):
        self.__key = np.array([[0, 0], [0, 0]]) # n x n matrix
        self.__maxScore = float("-inf")
        self.__trials = 0

        #read key dictionary file line by line, decoding as the lines are read
        with open("hill_2x2_keys.txt", "r") as f:
            hasKey = True
            while hasKey:
                line = f.readline().strip()
                if line != "":
                    #turn string key into nested list
                    line_list = line.split(" ")
                    self.__key = np.array([[line_list[0], line_list[1]], [line_list[2], line_list[3]]], dtype = int)

                    #decode cyphertext using current key
                    plaintext = self.decipher(cipher_text, self.__key)

                    #evaluate score of plaintext generated by key 
                    #(quadgram seemed to work the best for hill climb so I'm using it here as well. Although this should work with bigram or IOC)
                    score = evaluate.evaluateQuadgramFrequencies(plaintext)

                    if score > self.__maxScore:
                        self.__maxScore = score

                        #yield the current best plaintext
                        yield plaintext

                    self.__trials += 1
                else:
                    #ends subroutine once no keys are left in file
                    hasKey = False

if __name__ == "__main__":
    #test code

    #chapter 10A (2023)
    cipher_text = "HHIZR KHHXH XCFWL WJHIC YFPAX FHHZD VZLWJ HREXL CGWPP XUWSK EEQTP WDSCA ICHHZ DHVPQ NGAEU CNUAH VQJOV ILWJH VZCEL PLTLD NNNHR RPTQT AHXQE EUCGZ LPRFW QQUGZ WAVOW KGZCQ KKZNY ITMMM ASMQW APRPN IBHKL TRIYY QTTHH UWPLP THWHK GVITG HAWOA WVDGZ HALPJ RQTVI OWZGI CORHH ZDBPB JGKEF JOFWX QLPLT RIFMS KAHWO MYWOB JVXPX TZLEJ UEELE LPHKB UWKBP YRLPU IORVP LQICQ TRVQJ HVLEN APTQI PDBZD KKMZR IMEWA OVZAH NACEW EPRLO REGKA HXQBY BJWAP RPNIB HKVPG THAVI NAUQY WAEHH ZDWAR EFJTH VZVIA HASCC WABUZ GICOR FJAHT IVMJN VOXBL ETHFT LCKBI QRVWO EABOL DYWNA KWFWV MOUAT BPXYN GAERR FXAMX QWOLD BOAHG IXMLP KDBYT TQTSK AELTU WMEWA LTEMW HVZPT SKEEJ NLAFT BQLDH VLPAP AHQCB OAHFG GYXCF WGSBU PXXHM ABIVQ EECTE EBZMG MSWOX BDDUW LPXRP TGUEA TEEXP NHVLE KMDWH AHHUV NGNSA EKOTT LJMGB UBCJH TKNCB JJQVI LDWNA MAHJO SKXBK DRRVI IMSSL ELPAC RRMWB UUGOU ATJDM XASZR AMSGY RVJWA HVVCV QCAIC UITTA HSGPN BCICP LHHPL SKUIV IUIVD HHDDM GHWKM WKYJS KPLIM LMNGP WDGGZ NNTEH KLWEX LPHLT TTESS QTAHV MAWVM WOBJW HFKAW MGGVZ HWAAI GZLPA LIQGZ BYBJK YQTVM VJIUN AMAYR LPVZT KCKLD HHDDC TEEBZ KYBLH KBUIC FRYWF JAHCA EMWHK OBJGZ ICJQH VXBWH MEEAT EAPVW TBZGA HGIXM LPRRQ TOSZA JOFWA WAWRR JDHZS WZDPN BOWOV JFQEF EEMXX QGYIM VJEMP LFWCU ZUREN SAHCA CCGZS JEESA HVGZL PZQKG GZLPQ IVJFQ KRVQI MBPAG ATUAC QOPRK LPRER FYRLP BYVMK SWANA RFHJI CJBMU EMWHJ DMXAS ATLPH LTKNC TTMGM GLWVI AHQCE EGZUG LSVQE EXOEE AHZKL OYWAH CAXKK GVJPI RUWEI XFTTX CNGOG ZLPME AHICN UPWDS CAICT BOSKS ANMYB OYFRU MUDON AJPXQ SSZNH VXPBP OGVCV MWOVJ XFTZT HRRDK BUGIY PASFR SKZNY IVILQ FWWWU XHVWA MUTZM AUUUV PTVXS DCAVI AHWOG XVIPY RUMQ"
    hill_cipher = hill(cipher_text)

    for plaintext in hill_cipher.plainTexts():
        print("")
        print(plaintext)
        print(hill_cipher._hill__maxScore)
        print(hill_cipher._hill__key)
    
    """
    #worst case cypher
    cipher_text = "avdxislqsbriuaanrhklthxcienagspxxckmqityaxejisgg"
    hill_cipher = hill(cipher_text)

    for plaintext in hill_cipher.plainTexts():
        print("")
        print(plaintext)
        print(hill_cipher._hill__maxScore)
        print(hill_cipher._hill__key)
    """

