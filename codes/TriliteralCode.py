num = """
V4V4VVV444AV4AV444A44V4A44444A444AAA44A4VAA444A4444AAV
 VA4AAA44V4AVV44444VVA4AVV4A444A44V4V444A44V4A444A44V4V
 V4A44444A444AAA44A4VAA444A4444AAVVA4AAA44V4AVV44444V4A
 AV4AAA4AVVAV4VV4AVV444AV444A44AAV444V4V4VV44AV4V44444A
 AAV4A4A444AVAAVV4V444AAAVVAV4AV4VA444A4444V4VV44A44AAV
 A44V4VVVA444VVAAV4VA44444VA4AVV4V444V4V4VVV444AV4AV444
 44AV4A44444A444AAA44A4VAA444A4444AAVVA4AAA44V4AVV44444
 V4V4VV4AV444AVA44AV4AV4V44444AAAV4AA444V4V4VV4AV444AVA
 V444AVV4A4AVAAVV4V44444AAAV4AA444V4V4VV4AV4444V4VA4V4V
 VA4V444AV4444V444AA44V4V4VV44444AAAV4AA4444VVAV4AVA4AV
 44444AAAV4AA4444A44VV44AV44A44V4VVVA444V4V4VV4AV4444VV
 4AV44AV44V4V44444AAAV4AA444V4V4VV4AV44444VV4444AA44AAV
 44444AAAV4AA444V4V4VV4AV44444VAV44AAVVA4444VAA44VAA4AV
 444VVAAV4VA4444V4V4VVV444AV4AV44444AV4A44444A444AAA44A
 4VAA444A4444AAVVA4AAA44V4AVV44

"""
num = num.replace("\n", "")

codes1 = {
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

codes2 = {
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
# space=ccc
list1 = ''  # ABC
list2 = ''  # ACB
list3 = ''  # BAC
list4 = ''  # BCA
list5 = ''  # CAB
list6 = ''  # CBA
# space=aaa
list21 = ''  # ABC
list22 = ''  # ACB
list23 = ''  # BAC
list24 = ''  # BCA
list25 = ''  # CAB
list26 = ''  # CBA
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
                code1 += 'A'
            if valid2:
                code2 += 'A'
            if valid3:
                code3 += 'B'
            if valid4:
                code4 += 'B'
            if valid5:
                code5 += 'C'
            if valid6:
                code6 += 'C'
        elif i == charb:
            if valid1:
                code1 += 'B'
            if valid2:
                code2 += 'C'
            if valid3:
                code3 += 'A'
            if valid4:
                code4 += 'C'
            if valid5:
                code5 += 'A'
            if valid6:
                code6 += 'B'
        elif i == charc:
            if valid1:
                code1 += 'C'
            if valid2:
                code2 += 'B'
            if valid3:
                code3 += 'C'
            if valid4:
                code4 += 'A'
            if valid5:
                code5 += 'B'
            if valid6:
                code6 += 'A'
        if len(code1) == 3:
            try:
                list1 += codes1[code1]
                list21 += codes2[code1]
                code1 = ''
            except:
                valid1 = False
        if len(code2) == 3:
            try:
                list2 += codes1[code2]
                list22 += codes2[code2]
                code2 = ''
            except:
                valid2 = False
        if len(code3) == 3:
            try:
                list3 += codes1[code3]
                list23 += codes2[code3]
                code3 = ''
            except:
                valid3 = False
        if len(code4) == 3:
            try:
                list4 += codes1[code4]
                list24 += codes2[code4]
                code4 = ''
            except:
                valid4 = False
        if len(code5) == 3:
            try:
                list5 += codes1[code5]
                list25 += codes2[code5]
                code5 = ''
            except:
                valid5 = False
        if len(code6) == 3:
            try:
                list6 += codes1[code6]
                list26 += codes2[code6]
                code6 = ''
            except:
                valid6 = False

plaintextlist = []
if valid1:
    plaintextlist.append((list21,'Space AAA, code ABC'))
    plaintextlist.append((list1, 'Space CCC, code ABC'))
if valid2:
    plaintextlist.append((list22, 'Space AAA, code ACB'))
    plaintextlist.append((list2, 'Space CCC, code ABC'))
if valid3:
    plaintextlist.append((list23,'Space AAA, code BAC'))
    plaintextlist.append((list3, 'Space CCC, code ABC'))
if valid4:
    plaintextlist.append((list24,'Space AAA, code BCA'))
    plaintextlist.append((list4, 'Space CCC, code ABC'))
if valid5:
    plaintextlist.append((list25,'Space AAA, code CAB'))
    plaintextlist.append((list5, 'Space CCC, code ABC'))
if valid6:
    plaintextlist.append((list26,'Space AAA, code CBA'))
    plaintextlist.append((list6, 'Space CCC, code ABC'))

from math import inf
from formatCipher import intToString, stringToInt
from linguisticData.evaluate import evaluateQuadgramFrequencies

maxScore = -inf
for plainText in plaintextlist:
    score = evaluateQuadgramFrequencies(stringToInt(plainText[0]))
    code = plainText[1]
    # we should only tell the user if we've made progress
    if score > maxScore:
        print(plainText[0])
        print(score)
        print(code)
        maxScore = score
