num = """
BXBBBBXBXXBXBBBBXBXBBBXBBBBXBBBBBBBXBBXXBXBBBBXXBXBBXXBBBBXBBBXXXBBXBBBBXBBXBBXXBXXXBXBBXB
"""
num = num.replace("\n", "")

codes = {
    'AAAAA' : 'A',
    'ABAAB' : 'J',
    'BAABA' : 'S',
    'AAAAB' : 'B',
    'ABABA' : 'K',
    'BAABB' : 'T',
    'AAABA' : 'C',
    'ABABB' : 'L',
    'BABAA' : 'U',
    'AAABB' : 'D',
    'ABBAA' : 'M',
    'BABAB' : 'V',
    'AABAA' : 'E',
    'ABBAB' : 'N',
    'BABBA' : 'W',
    'AABAB' : 'F',
    'ABBBA' : 'O',
    'BABBB' : 'X',
    'AABBA' : 'G',
    'ABBBB' : 'P',
    'BBAAA' : 'Y',
    'AABBB' : 'H',
    'BAAAA' : 'Q',
    'BBAAB' : 'Z',
    'ABAAA' : 'I',
    'BAAAB' : 'R'
}
lista = ''
listb = ''
codea = ''
codeb = ''
chara = ''
charb = ''
avalid = True
bvalid = True

for f in num:
    if f != ' ':
        if not chara:
            chara = f
        elif not charb and f != chara:
            charb = f
            break

for i in num:
    if i != ' ':
        if i == chara:
            if avalid:
                codea+='A'
            if bvalid:
                codeb+='B'
        elif i == charb:
            if avalid:
                codea+='B'
            if bvalid:
                codeb+='A'
        if len(codea) == 5:
            try:
                lista+=codes[codea]
                codea = ''
            except:
                avalid = False
        if len(codeb) == 5:
            try:
                listb+=codes[codeb]
                codeb = ''
            except:
                bvalid = False

if avalid:
    print(chara,'= A')
    print(charb,'= B')
    print(lista)
if bvalid:
    print(charb,'= A')
    print(chara,'= B')
    print(listb)
if not avalid and not bvalid:
    print('False')