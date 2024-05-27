
def evaluateBigramFrequencies(plainText):
    window = plainText[ :2]
    fitness = 0
    for letter in plainText[2: ]:
        try:
            fitness += idealBigramFreqs[window]
        except:
            fitness += floor
        window = window[1:] + letter

    return fitness


def int_to_char(charCode):
    return chr(charCode + 97)

def char_to_int(char):
    return ord(char) - 97

def gcd(a, b):
    while b:
        a, b = b, a % b

    return a

class hill():
    def __init__(self, ciphertext, testChunk):
        self.__ciphertext = ciphertext
        self.__testChunk = testChunk
    
    def __calc_det(self, key_matrix):
        return (key_matrix[0][0] * key_matrix[1][1]) - (key_matrix[0][1] * key_matrix[1][0])
    
    def __mod_inverse(self, det):
        det = (det % 26 + 26) % 26

        for i in range(1, 26):
            if (det * i) % 26 == 1:
                return i

        return -1
    
    def __is_valid_key(self, key):
        determinant = self.__calc_det(key) % 26
        return determinant != 0 and gcd(determinant, 26) == 1

    def __mod_matrix_inv(self, matrix):
        intDet = self.__calc_det(matrix)
        det_inv = self.__mod_inverse(intDet)

        adjugate = [
            [matrix[1][1], -matrix[0][1]],
            [-matrix[1][0], matrix[0][0]]
        ]

        moduloMatrixInv = [[], []]
        for i in range(2):
            for j in range(2):
                moduloMatrixInv[i].append(((adjugate[i][j] * det_inv) % 26 + 26) % 26)

        return moduloMatrixInv

    def decipher(self, inv_key, length):
        plaintext = ""

        for i in range(0, length, 2):
            left_val = char_to_int(self.__ciphertext[i])
            right_val = char_to_int(self.__ciphertext[i + 1])

            plaintext += int_to_char((inv_key[0][0] * left_val + inv_key[0][1] * right_val) % 26)
            plaintext += int_to_char((inv_key[1][0] * left_val + inv_key[1][1] * right_val) % 26)

        return plaintext
    
    def __printEncryptionSet(self, inv_key, score):
        full_plaintext = self.decipher(inv_key, len(self.__ciphertext))

        key = self.__mod_matrix_inv(inv_key)

        print(full_plaintext[ :20], "...")
        print("Score:", score)
        print("Key:")
        print(key[0][0], key[0][1])
        print(key[1][0], key[1][1])

    def keyDictAttack(self):
        self.__maxScore = float("inf")
        self.__trials = 0
        self.__bestKey = None

        for a in range(0, 25):
            for b in range(0, 25):
                for c in range(0, 25):
                    for d in range(0, 25):
                        key = [[a, b], [c, d]]
                        if self.__is_valid_key(key):
                            inv_key = self.__mod_matrix_inv(key)

                            plaintext = self.decipher(inv_key, self.__testChunk)

                            score = evaluateBigramFrequencies(plaintext)

                            if score < self.__maxScore:
                                self.__maxScore = score
                                self.__bestKey = inv_key

                            self.__trials += 1


        print("Best result:")
        self.__printEncryptionSet(self.__bestKey, self.__maxScore)

        print("Total number of trials:", self.__trials)



floor = 20

idealBigramFreqs = {"th": 1, "hm": 7, "mr": 6, "rs": 4, "sf": 6, "fe": 5, "er": 2, "rr": 6, "ra": 4, "ar": 3, "sd": 7, "di": 3, "ie": 5, "ed": 2, "do": 4, "on": 3, "nt": 2, "he": 1, "en": 2, "ni": 4, "ig": 5, "gh": 4, "ht": 4, "to": 2, "of": 3, "ft": 4, "et": 3, "hs": 7, "se": 3, "ep": 4, "pt": 6, "te": 3, "em": 4, "mb": 6, "be": 4, "at": 2, "hu": 7, "ur": 4, "da": 4, "ay": 5, "yi": 5, "iw": 6, "wa": 3, "as": 3, "ss": 4, "tf": 6, "fo": 4, "or": 3, "ei": 4, "oc": 6, "cl": 6, "lo": 4, "ck": 5, "ko": 8, "mo": 4, "rn": 5, "in": 2, "ng": 3, "go": 5, "ff": 6, "fr": 5, "ri": 4, "id": 4, "yt": 5, "re": 2, "ew": 4, "sn": 6, "no": 3, "ot": 3, "hi": 3, "gt": 5, "ob": 6, "ne": 3, "es": 2, "sh": 3, "eh": 4, "ha": 2, "ad": 4, "db": 5, "ee": 4, "nd": 2, "de": 4, "ea": 3, "ds": 5, "so": 4, "om": 4, "me": 3, "ho": 4, "ou": 2, "si": 4, "it": 3, "tw": 4, "sj": 9, "ju": 7, "us": 4, "st": 3, "ta": 3, "af": 6, "wm": 8, "mi": 5, "nu": 7, "ut": 4, "sa": 3, "wh": 4, "ir": 4, "ac": 4, "ch": 4, "dh": 5, "eo": 4, "nc": 5, "ce": 4, "io": 5, "op": 5, "pe": 4, "dt": 4, "ef": 4, "ro": 3, "td": 6, "oo": 4, "rw": 6, "wi": 4, "my": 5, "yl": 7, "la": 4, "tc": 6, "hk": 12, "ke": 4, "ey": 5, "ya": 5, "an": 2, "dp": 6, "pu": 7, "rp": 6, "po": 4, "os": 4, "el": 3, "ly": 4, "yd": 7, "ye": 5, "ts": 4, "al": 3, "ll": 3, "lh": 7, "gi": 5, "gu": 7, "up": 5, "pm": 10, "yh": 6, "li": 4, "ov": 6, "ve": 3, "rc": 6, "co": 4, "oa": 6, "tt": 3, "ti": 3, "ih": 6, "dd": 6, "aw": 6, "is": 3, "pr": 5, "ec": 4, "ca": 4, "au": 6, "na": 4, "ag": 5, "ga": 5, "ai": 4, "ns": 4, "il": 4, "fa": 5, "rl": 6, "tu": 5, "um": 6, "mn": 8, "nm": 6, "lt": 5, "tr": 5, "ru": 6, "sc": 5, "ab": 5, "bl": 5, "yu": 9, "ps": 7, "dw": 5, "wo": 5, "ia": 5, "am": 4, "tg": 8, "oi": 5, "tm": 6, "if": 5, "wt": 7, "ev": 5, "ex": 6, "xt": 8, "ww": 8, "we": 4, "ek": 7, "ks": 7, "mp": 6, "ph": 7, "ic": 4, "dn": 5, "bu": 5, "ct": 5, "ol": 5, "ld": 4, "dm": 6, "im": 4, "ah": 7, "df": 6, "mt": 6, "gr": 6, "le": 3, "tl": 5, "cu": 6, "rt": 4, "dr": 5, "ry": 5, "yc": 7, "ug": 5, "fm": 7, "ys": 5, "ty": 5, "yo": 4, "uj": 12, "ja": 8, "un": 4, "nn": 6, "yq": 11, "qu": 6, "ue": 6, "oe": 7, "ls": 6, "ul": 4, "tb": 6, "sp": 5, "ci": 6, "ym": 6, "ow": 4, "yf": 7, "rk": 6, "ki": 5, "ip": 7, "pl": 5, "su": 5, "sg": 7, "fi": 5, "fc": 8, "cr": 6, "dc": 7, "nl": 6, "gg": 8, "ge": 4, "pa": 5, "tp": 7, "ny": 6, "by": 6, "gp": 9, "dl": 6, "tk": 8, "kn": 6, "ws": 7, "ma": 4, "rv": 7, "va": 7, "sm": 5, "sw": 5, "eg": 5, "og": 6, "nf": 6, "rm": 5, "nb": 7, "az": 9, "zi": 9, "gl": 6, "xp": 7, "sr": 7, "sl": 6, "tn": 7, "fh": 7, "hw": 7, "gm": 7, "gs": 6, "nw": 6, "wc": 10, "mm": 7, "nk": 6, "wl": 8, "dg": 7, "vi": 6, "nh": 5, "lf": 6, "ap": 5, "lm": 7, "av": 5, "bi": 7, "ua": 6, "yw": 6, "hh": 7, "np": 7, "ib": 7, "eu": 6, "tj": 9, "eb": 5, "fk": 11, "sb": 6, "ba": 6, "dj": 8, "ms": 6, "nv": 8, "ej": 8, "jo": 8, "rf": 6, "lp": 7, "du": 6, "lg": 9, "lc": 8, "oh": 6, "cb": 12, "sy": 7, "fg": 9, "ik": 6, "cc": 7, "nq": 9, "ui": 6, "uv": 10, "yg": 8, "ok": 5, "ka": 7, "rd": 5, "hn": 8, "iv": 5, "lw": 7, "lb": 8, "fw": 8, "uy": 10, "yp": 7, "rh": 6, "od": 5, "hr": 7, "sv": 8, "vo": 7, "ud": 7, "hy": 7, "uc": 6, "rb": 6, "br": 6, "ak": 6, "kf": 9, "oz": 9, "ze": 8, "sq": 9, "lk": 7, "mg": 10, "wn": 6, "dy": 6, "lr": 8, "dk": 9, "km": 9, "wd": 9, "uk": 8, "xc": 8, "gw": 7, "mu": 6, "pi": 6, "oy": 6, "pp": 6, "fu": 6, "lu": 7, "ii": 10, "bo": 5, "fv": 11, "uh": 8, "fy": 8, "fd": 9, "gn": 7, "wf": 10, "yy": 8, "lv": 8, "nj": 9, "bs": 8, "ix": 9, "xm": 13, "pw": 9, "kh": 8, "hg": 10, "ky": 8, "bj": 9, "je": 8, "uf": 8, "fn": 10, "fp": 8, "yk": 9, "ub": 7, "bt": 9, "hl": 8, "pf": 10, "kc": 10, "ml": 9, "wr": 7, "yb": 6, "kt": 7, "nr": 8, "kv": 12, "fs": 7, "sk": 6, "ao": 9, "bb": 9, "rg": 6, "kl": 8, "yr": 7, "kr": 9, "gb": 8, "vu": 12, "kw": 8, "hf": 9, "xy": 13, "cs": 9, "dv": 8, "hp": 9, "gy": 9, "yn": 7, "cy": 9, "fl": 7, "mc": 9, "xa": 8, "eq": 8, "wy": 9, "hc": 9, "dq": 10, "md": 10, "gv": 10, "wk": 11, "lj": 11, "kb": 9, "iz": 8, "uz": 10, "zz": 10, "zl": 11, "gf": 8, "pb": 10, "ln": 9, "gd": 9, "uw": 8, "hb": 8, "ku": 10, "fb": 8, "rj": 9, "aq": 10, "wv": 11, "hd": 9, "mf": 9, "yv": 9, "aa": 8, "cq": 10, "mw": 8, "vy": 11, "pc": 11, "ae": 10, "uu": 11, "rq": 10, "mh": 8, "hq": 13, "oq": 11, "nx": 11, "xi": 8, "gq": 12, "iu": 9, "kg": 11, "yj": 10, "uo": 10, "tq": 10, "wp": 9, "tv": 9, "hv": 11, "xf": 12, "xe": 10, "wb": 10, "bc": 13, "oj": 10, "gc": 9, "mq": 12, "aj": 10, "xq": 13, "py": 9, "ez": 9, "wu": 11, "cp": 12, "kq": 14, "gz": 15, "za": 8, "ax": 10, "lq": 12, "kp": 10, "zh": 12, "wg": 12, "bh": 12, "gj": 11, "hj": 11, "gk": 12, "wq": 13, "kk": 12, "bm": 12, "kd": 10, "bv": 11, "mj": 11, "iq": 11, "pn": 11, "fq": 13, "xh": 11, "uq": 13, "fj": 11, "xj": 16, "lx": 19, "ux": 12, "pd": 12, "ox": 10, "xs": 12, "pk": 13, "ij": 11, "pj": 14, "mk": 12, "cw": 11, "cd": 12, "pg": 13, "mv": 11, "xo": 12, "xu": 12, "cz": 16, "cf": 12, "zv": 14, "ji": 12, "cm": 12, "iy": 13, "wj": 12, "zs": 11, "kj": 12, "bf": 13, "bq": 18, "zo": 10, "cj": 15, "xw": 12, "pv": 14, "rz": 12, "xb": 14, "cg": 12, "xl": 13, "zp": 14, "bn": 13, "zu": 12, "yz": 14, "bw": 12, "bp": 15, "nz": 11, "zy": 12, "cn": 13, "bd": 12, "xn": 14, "qs": 17, "jg": 19, "pq": 15, "vr": 14, "vn": 14, "lz": 14, "dz": 14, "xr": 14, "cv": 15, "vk": 15, "xd": 14, "tz": 11, "zt": 11, "zn": 13, "zm": 13, "sx": 19, "xv": 16, "vs": 12, "xk": 16, "xg": 15, "sz": 13, "hz": 17, "vb": 15, "vc": 14, "vj": 17, "jd": 19, "vt": 14, "jk": 19, "jw": 19, "js": 19, "jc": 19, "vm": 16, "qp": 18, "qc": 18, "vw": 14, "vd": 15, "vh": 14, "vf": 16, "qo": 18, "bk": 16, "bg": 16, "zr": 11, "jj": 19, "jy": 19, "zw": 11, "fz": 15, "zc": 13, "zd": 13, "yx": 16, "wz": 18, "zb": 13, "qb": 19, "vv": 17, "zj": 16, "jz": 16, "qt": 17, "rx": 15, "qa": 19, "vp": 15, "zf": 14, "vl": 15, "pz": 17, "zk": 15, "tx": 19, "zg": 14, "dx": 17, "zq": 15, "kz": 19, "jr": 18, "jt": 14, "fx": 18, "vg": 17, "mz": 19, "qr": 19}

#chapter 10A (2023)
ciphertext = "hhizrkhhxhxcfwlwjhicyfpaxfhhzdvzlwjhrexlcgwppxuwskeeqtpwdscaichhzdhvpqngaeucnuahvqjovilwjhvzcelpltldnnnhrrptqtahxqeeucgzlprfwqqugzwavowkgzcqkkznyitmmmasmqwaprpnibhkltriyyqtthhuwplpthwhkgvitghawoawvdgzhalpjrqtviowzgicorhhzdbpbjgkefjofwxqlpltrifmskahwomywobjvxpxtzlejueelelphkbuwkbpyrlpuiorvplqicqtrvqjhvlenaptqipdbzdkkmzrimewaovzahnaceweprloregkahxqbybjwaprpnibhkvpgthavinauqywaehhzdwarefjthvzviahasccwabuzgicorfjahtivmjnvoxblethftlckbiqrvwoeaboldywnakwfwvmouatbpxyngaerrfxamxqwoldboahgixmlpkdbyttqtskaeltuwmewaltemwhvzptskeejnlaftbqldhvlpapahqcboahfggyxcfwgsbupxxhmabivqeecteebzmgmswoxbdduwlpxrptgueateexpnhvlekmdwhahhuvngnsaekottljmgbubcjhtkncbjjqvildwnamahjoskxbkdrrviimsslelpacrrmwbuugouatjdmxaszramsgyrvjwahvvcvqcaicuittahsgpnbcicplhhplskuiviuivdhhddmghwkmwkyjskplimlmngpwdggznntehklwexlphltttessqtahvmawvmwobjwhfkawmggvzhwaaigzlpaliqgzbybjkyqtvmvjiunamayrlpvztkckldhhddcteebzkyblhkbuicfrywfjahcaemwhkobjgzicjqhvxbwhmeeateapvwtbzgahgixmlprrqtoszajofwawawrrjdhzswzdpnbowovjfqefeemxxqgyimvjemplfwcuzurensahcaccgzsjeesahvgzlpzqkggzlpqivjfqkrvqimbpagatuacqoprklprerfyrlpbyvmkswanarfhjicjbmuemwhjdmxasatlphltkncttmgmglwviahqceegzuglsvqeexoeeahzkloywahcaxkkgvjpiruweixfttxcngogzlpmeahicnupwdscaictbosksanmyboyfrumudonajpxqssznhvxpbpogvcvmwovjxftzthrrdkbugiypasfrskznyivilqfwwwuxhvwamutzmauuuvptvxsdcaviahwogxvipyrumq"

hill_cipher = hill(ciphertext, 19)

hill_cipher.keyDictAttack()
