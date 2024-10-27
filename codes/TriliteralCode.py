from formatCipher import stringToInt, intToString

class triliteralDecoder():  # also name the file the same way please

    def __init__(self, cipher):
        cipher = cipher.replace("\n", "")
        self.__cipher = cipher  # the cipherText
        self.codes1 = {
            'AAA': 'A',
            'BAA': 'J',
            'CAA': 'S',
            'AAB': 'B',
            'BAB': 'K',
            'CAB': 'T',
            'AAC': 'C',
            'BAC': 'L',
            'CAC': 'U',
            'ABA': 'D',
            'BBA': 'M',
            'CBA': 'V',
            'ABB': 'E',
            'BBB': 'N',
            'CBB': 'W',
            'ABC': 'F',
            'BBC': 'O',
            'CBC': 'X',
            'ACA': 'G',
            'BCA': 'P',
            'CCA': 'Y',
            'ACB': 'H',
            'BCB': 'Q',
            'CCB': 'Z',
            'ACC': 'I',
            'BCC': 'R',
            'CCC': ' '
        }

        self.codes2 = {
            'AAA': ' ',
            'BAA': 'I',
            'CAA': 'R',
            'AAB': 'A',
            'BAB': 'J',
            'CAB': 'S',
            'AAC': 'B',
            'BAC': 'K',
            'CAC': 'T',
            'ABA': 'C',
            'BBA': 'L',
            'CBA': 'U',
            'ABB': 'D',
            'BBB': 'M',
            'CBB': 'V',
            'ABC': 'E',
            'BBC': 'N',
            'CBC': 'W',
            'ACA': 'F',
            'BCA': 'O',
            'CCA': 'X',
            'ACB': 'G',
            'BCB': 'P',
            'CCB': 'Y',
            'ACC': 'H',
            'BCC': 'Q',
            'CCC': 'Z'
        }

        #Find three characters
        chara = ''
        charb = ''
        charc = ''
        for f in cipher:
            if f != ' ' and f != '':
                if not chara:
                    chara = f
                elif not charb and f != chara:
                    charb = f
                elif not charc and f != charb and f != chara:
                    charc = f
                    break
        self.listOfKeys = [
            [chara,charb,charc,'A'],
            [chara, charc, charb,'A'],
            [charb, chara, charc,'A'],
            [charb, charc, chara,'A'],
            [charc, chara, charb,'A'],
            [charc, charb, chara,'A'],
            [chara, charb, charc,'C'],
            [chara, charc, charb,'C'],
            [charb, chara, charc,'C'],
            [charb, charc, chara,'C'],
            [charc, chara, charb,'C'],
            [charc, charb, chara,'C']
        ]


    def plainTexts(self):
        for keys in self.listOfKeys:
            code = ''
            plainText = ''
            for char in self.__cipher:
                if char == keys[0]:
                    code+='A'
                elif char == keys[1]:
                    code+='B'
                elif char == keys[2]:
                    code+='C'
                if len(code) == 3:
                    try:
                        if keys[3] == 'A':
                            plainText += self.codes1[code]
                        if keys[3] == 'C':
                            plainText += self.codes2[code]
                        code = ''
                    except:
                        continue
            plainText = stringToInt(plainText)
            yield plainText
