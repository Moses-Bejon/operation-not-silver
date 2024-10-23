num = """
ACCCCCBACACCBABABBCCCABBAAACABACCBBBACACCCAACACBABBABBCABBBCCAA
"""
num = num.replace("\n", "")

codes1 = {
    'AAA' : 'A',
    'BAA' : 'J',
    'CAA' : 'S',
    'AAB' : 'B',
    'BAB' : 'K',
    'CAB' : 'T',
    'AAC' : 'C',
    'BAC' : 'L',
    'CAC' : 'U',
    'ABA' : 'D',
    'BBA' : 'M',
    'CBA' : 'V',
    'ABB' : 'E',
    'BBB' : 'N',
    'CBB' : 'W',
    'ABC' : 'F',
    'BBC' : 'O',
    'CBC' : 'X',
    'ACA' : 'G',
    'BCA' : 'P',
    'CCA' : 'Y',
    'ACB' : 'H',
    'BCB' : 'Q',
    'CCB' : 'Z',
    'ACC' : 'I',
    'BCC' : 'R',
    'CCC' : ' '
}

codes2 = {
    'AAA' : ' ',
    'BAA' : 'I',
    'CAA' : 'R',
    'AAB' : 'A',
    'BAB' : 'J',
    'CAB' : 'S',
    'AAC' : 'B',
    'BAC' : 'K',
    'CAC' : 'T',
    'ABA' : 'C',
    'BBA' : 'L',
    'CBA' : 'U',
    'ABB' : 'D',
    'BBB' : 'M',
    'CBB' : 'V',
    'ABC' : 'E',
    'BBC' : 'N',
    'CBC' : 'W',
    'ACA' : 'F',
    'BCA' : 'O',
    'CCA' : 'X',
    'ACB' : 'G',
    'BCB' : 'P',
    'CCB' : 'Y',
    'ACC' : 'H',
    'BCC' : 'Q',
    'CCC' : 'Z'
}
#space=ccc
list1 = '' #ABC
list2 = '' #ACB
list3 = '' #BAC
list4 = '' #BCA
list5 = '' #CAB
list6 = '' #CBA
#space=aaa
list21 = '' #ABC
list22 = '' #ACB
list23 = '' #BAC
list24 = '' #BCA
list25 = '' #CAB
list26 = '' #CBA
code1 = ''
code2 = ''
code3 = ''
code4 = ''
code5 = ''
code6 = ''
chara = ''
charb = ''
charc = ''
valid1 = True
valid2 = True
valid3 = True
valid4 = True
valid5 = True
valid6 = True

for f in num:
    if f != ' ':
        if not chara:
            chara = f
        elif not charb and f != chara:
            charb = f
        elif not charc and f != charb and f != chara:
            charc = f
            break

for i in num:
    if i != ' ':
        if i == chara:
            if valid1:
                code1+='A'
            if valid2:
                code2+='A'
            if valid3:
                code3+='B'
            if valid4:
                code4+='B'
            if valid5:
                code5+='C'
            if valid6:
                code6+='C'
        elif i == charb:
            if valid1:
                code1+='B'
            if valid2:
                code2+='C'
            if valid3:
                code3+='A'
            if valid4:
                code4+='C'
            if valid5:
                code5+='A'
            if valid6:
                code6+='B'
        elif i == charc:
            if valid1:
                code1+='C'
            if valid2:
                code2+='B'
            if valid3:
                code3+='C'
            if valid4:
                code4+='A'
            if valid5:
                code5+='B'
            if valid6:
                code6+='A'
        if len(code1) == 3:
            try:
                list1+=codes1[code1]
                list21+=codes2[code1]
                code1 = ''
            except:
                valid1 = False
        if len(code2) == 3:
            try:
                list2+=codes1[code2]
                list22+=codes2[code2]
                code2 = ''
            except:
                valid2 = False
        if len(code3) == 3:
            try:
                list3+=codes1[code3]
                list23+=codes2[code3]
                code3 = ''
            except:
                valid3 = False
        if len(code4) == 3:
            try:
                list4+=codes1[code4]
                list24+=codes2[code4]
                code4 = ''
            except:
                valid4 = False
        if len(code5) == 3:
            try:
                list5+=codes1[code5]
                list25+=codes2[code5]
                code5 = ''
            except:
                valid5 = False
        if len(code6) == 3:
            try:
                list6+=codes1[code6]
                list26+=codes2[code6]
                code6 = ''
            except:
                valid6 = False
        
print('\n\nSPACE = CCC\n\n')
if valid1:
    print(chara,'= A')
    print(charb,'= B')
    print(charc,'= C')
    print(list1)
if valid2:
    print(chara,'= A')
    print(charc,'= B')
    print(charb,'= C')
    print(list2)
if valid3:
    print(charb,'= A')
    print(chara,'= B')
    print(charc,'= C')
    print(list3)
if valid4:
    print(charb,'= A')
    print(charc,'= B')
    print(chara,'= C')
    print(list4)
if valid5:
    print(charc,'= A')
    print(chara,'= B')
    print(charb,'= C')
    print(list5)
if valid6:
    print(charc,'= A')
    print(charb,'= B')
    print(chara,'= C')
    print(list6)

if not(valid6 or valid1 or valid2 or valid3 or valid4 or valid5):
    print('False')

print('\n\nSPACE = AAA\n\n')
if valid1:
    print(chara,'= A')
    print(charb,'= B')
    print(charc,'= C')
    print(list21)
if valid2:
    print(chara,'= A')
    print(charc,'= B')
    print(charb,'= C')
    print(list22)
if valid3:
    print(charb,'= A')
    print(chara,'= B')
    print(charc,'= C')
    print(list23)
if valid4:
    print(charb,'= A')
    print(charc,'= B')
    print(chara,'= C')
    print(list24)
if valid5:
    print(charc,'= A')
    print(chara,'= B')
    print(charb,'= C')
    print(list25)
if valid6:
    print(charc,'= A')
    print(charb,'= B')
    print(chara,'= C')
    print(list26)

if not(valid6 or valid1 or valid2 or valid3 or valid4 or valid5):
    print('False')
