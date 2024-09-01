from formatCipher import stringToInt, intToString
from linguisticData.evaluate import *
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

"""Instructions: for testing functionality, uncomment the relevant ciphertexts in main(). """

def lengthOperations(ciphertext): # might end up being a class!
    l = len(ciphertext)
    lengthRooted = l**0.5
    lengthCubeRooted = l**(1/3)
    lengthFactors = set() 
    currLength = l
    for i in range(1, int(lengthRooted)+1):
        if currLength % i == 0:
            lengthFactors.add(i)
            lengthFactors.add(currLength//i)
    lengthFactors = sorted(lengthFactors)
    print("Factors of length: ", lengthFactors) # factors are useful because for ciphers like Hill e.g. 3x3 means length of ciphertext must be multiple of 3 to fit the matmul operations.


def IOC(ciphertext, block=1, times_entropy=False):
    original = ciphertext[:]    
    # divide into blocks of size block like madness p.31- IN PROGRESS
    # --------------------------------------------------------
    ciphertext = [
        tuple(ciphertext[start:start+block])
        for start in range(0, len(ciphertext), block)
    ]
    # print(ciphertext)
    counter = Counter(ciphertext)
    blockFrequencies = counter.values()
    # --------------------------------------------------------
    
    # letterFrequencies, total = getLetterFrequencies(original)
    ioc = getIOC(blockFrequencies, counter.total()) # not normalised
    if times_entropy:
        entropy = getEntropy(normaliseLetterFrequencies(blockFrequencies,counter.total()))
        return entropy*ioc
    return ioc

# to work with a general evalOverPeriods, we create new functions for the options so the graph title can use evaluator.__name__ for the plot title
def IOCTimesEntropy(ciphertext):
    return IOC(ciphertext, times_entropy=True)

def IOCBlock(ciphertext): # but breaks down here...
    return IOC(ciphertext, times_entropy=True)


# functionality to detect possible polyalphabetic periodic ciphers
def evalOverPeriods(ciphertext, evaluator, maxPeriod=30):
    results = []
    periods = [] # string, for plt to not do decimals in x axis
    for period in range(1, maxPeriod+1, 1):
        aggregate = 0 # for period of 4, abcd efgh we'll check ioc 4 times for ae, bf, cg, dh
        for starting in range(period):
            everyNthtext = ciphertext[starting::period] # array[start:stop:step]
            if len(everyNthtext) > 0: # how to prevent error with quadgram?? TODO: fix in py
                print(intToString(everyNthtext))
                aggregate += evaluator(everyNthtext) # add the score
            else:
                break
        aggregate /= period # we calculated as many IOCs as the length of the period and averaged
        results.append(aggregate) 
        periods.append(str(period))

    
    # print(results)
    plt.xlabel("Period")
    plt.ylabel("Result")
    plt.title(evaluator.__name__ + " over periods")
    plt.bar(periods, results)
    plt.show()

def main():
    # -----------INPUT CIPHERTEXT--------------
    # playfair for bigram IOC
    ciphertext = "MSFAPTTLIFKOFHDWPDMUDWCTFGHNRZMSOLTOIMSLLTCVFDEPZSBLKOGOEHMSDWZSSGVGFTOKBNDBSKDZTSKSRSLSONKFAFWGSTTCMSCPUCMQFDDLQLLSHUONKFAFIUWMQZQNSDMSBCQMBEZTMKTEPTLGSZOMKOZCOKIUGOGTDTXMWDBNFVKOGQZSLZPGBKNHGNQBBEBKBWPMNQEIPEOQBGGLCTOGOTBWDZNOMSXCQUPOSHWGGTTMLGKFQKDWGNDWALHULOWCHMSDSRUFSKDZBDEZNWVCHVPFMQQLKOQURSAFWENHEFANNQLQRUWGDLVFNOFEGRETOMDWGBIUIEFEQURELGCPUSDLGRWLSGSQSIGWKFGTUFQKKOEQIFBGIEHULSGLGZQFKOLOKFAFHZENKGEQLGIMQLQLFEGVBEOLTPKAQBTLOKIDZODFENKFGRZEALHUFEAFNOKFSFSBLQPEKSCBQYPCIUWNLSPDDLZSGKTOBWDZXMSGQZQLLSQLLGQUPTKYFGLFGTOFWDDLMSAFELLGBALSZTFHSBYOKSWNFVEFQLFSCPIKFGTOLGDBOKPDLFTPLPKFSZOMKOVMNQQIKFYRMSGNNMEFDWGNQUPOQBSDUPMBOGKFFVQTPGBKLGFDZKBGTSPNPTYMGLCPURYOOGFPFKKOFSKOHSSGODQSSDOPFBUFDFNQZTFHZSOPGBVMQBEFSFEFCPWDNOKFEFIUGUSWGHABDTCVFDHNNOLSLGMSOLDZKZQLUSBEQLOGNQVGQNTSHFTZGSQYOKDFIEHSQSSLLZKFPOKFYKQBTLOKSMSWMSBSSDGUSDWGDLTFCVMSBUABSKIEKOMSNQWBEFICCPPCIUWNLSONETNFVKBGMSABAFVCIUIEHGKGCWHSIYSKOMLGMSQLFOFDVKZEDPSRWOKFOKMSQLMWIFMNWMDBFNPTTLIELGMWGRUFOKLZKFSQURHWIZSTGKMDFGDLFDSELQKOGWPDYRGRDZPCNOOPKFOYGSDFSPQYQMOGQNSKVFIUGOGBDLGWQLOGZSGHABDZUGLOFDZKGWPDTOLGOPHFFEGWLSGOPEETSDMSAEPTEQSKNWWCTFLSPOMBMSBEKOBKDWEOMSGLSKDWPTEODZKZHUTFBWSLBNONQNSKOPEUEQSKGUTSGXPLMQNOSFSYNOQTFOCPFHPTURYOSQYOSLZKCVFDAFIGFSNHGLOKATOKVFOKEPPMFBPNNQFBLMPSMSEGNMEFNWWCTFKOFUFGEFGBGULPGRUZNOPCSBLQWBKRLOURSGHUOGRSLOMNOGSFSLLGDFNQZTHUHUOTBDRSEPTOTSUSPMCVEQSKQLUSBEKFWMPDDZDPHWOMZTCVFDHFTZDWZSHUOFDRLGGOSWOUEWKGYONQXMDZKFWSSEKSCQBDOULPKFABYCLSPNPCQVOFBNDZKFGULPPFCQMBIEFHFEPDAFYCQLLSUFETQFKOCPKSMSGLTOFBONKFAFMGCPLGEPYCWNFVEFESNBLGKFOCLSZTZRPGAFNQMSAUFKMBEFFAQBNWMBDFCQSBLQKZGRETOKGDCPQMBALOFBONVFYREFBNDZKFPNNHSBLQ"
    
    # 2x2 hill - to test IOC for n-gram blocks. Uncomment, compare this and the 3x3. You should find that the 3x3 has a high trigram fit and 2x2 has high bigram fit.

    # ciphertext = "Fhrtzp jqy fkvkr htno uj iqaf jbtz, iqu ejii dseiuo mmojj uj fvlyclysa yrfk uyo fvxv vdkr on. Jqoz an mcs eiuys, k gsekdt fvx, cl azgqb dyo wvjjgba gpjm, oh unf sgyuzc azoz iqu raocl xb ilpdrtozcq dcas fvlyclysk, rfvr nyo ixo, mh unf ozt fx enf rjs, wakzp xb vdgm on. Azoz A cab Fnpce, G svztlfxbqr jqmp Q jgb nzkr ozdpjjd yvpi isekdr jqc. C ydny otowjkrmmd yfvl Z fvrw’d comirun jqa bvpha mce, gf dvpir anlzkahtlzkd uj jqk huwa yz aefxnvxii pqetozfl iqc bdvm fsfclg.J"

    # 3x3 hill
    # ciphertext = "Yj g xpvtp xkhmw jkzvlyk mau gpdtaju puxlkxrrdvu, Fzlvc pmxcr khmnxns ta wp wnmblvf vdfjcpsgqrz. Ddk limulp xjo lky uw nymhsytg pplu, bse cgg bkpx, ljo lws gbcvchk yj g znvxarnc hedowli ivwrvrh, iliqwkt uzlv yj g zufids, bsrkc qa o ooxyc’f cttn urkmh ctgn dvxj, rtjzfl jjvczdptgt. Wobw xunpclr djluhbe ldo ppmpp rhn tngp, wicche talefvzp s vdcpyk mzpbxi. Nkh mamq aww ilqebk vphz pfem mqm wbjlsz sedojw, xtr zv rxa vaesmq vgrltf, qztndkksf mxkzqm vedo pdo. Prh xsl yxu znhtu fy khmh? Ixe kapbj zhhntj vphq awi ridnjubi kz ioxyljjl, zni poa bii wqtij rirz apx oby auttng bo pfrpexwsgfvzs xyk xovdftqzpnb. Bola usdw, hsd uztp idsomii xaml, qhx nf mxvann q ddwhoj uggapi--Ba. Uqjvh, nfh vfrs-pszmhcx mcrkdyjmd yk ooi nmdmrbo. Btgn khm hxhb mbofs pmp wsqhvbab mqquf, ltj tntrdnjrvu Fzlvy. “Vef’f rfkbu, vydk. L"
    # a random vigenere with key length 4
    # ciphertext = "WZEALYESUWCNSZEWLKARHLHTGGFJQURDSLISJSLUKSBJWACYHPTBKWRJHSCMOWTYHJOKWZEUOSISWWXYLKESFGDJGOIYKSDNIXEWHFTHDWSFUUIUKWRBKGSJLFCWHEESWASIHLEWPANJGTYYKWCTUJEXSGNILFGQHLTJ"
    # ciphertext = "zebra f"
    # -----------basic stats + checking format----------
    ciphertext = stringToInt(ciphertext)
    # print(ciphertext) 
    lengthOperations(ciphertext)
    evalLetterFreq = evaluateLetterFrequenciesUnsubstituted(ciphertext)
    print("Monogram fitness", evalLetterFreq)
    letterFrequencies, total = getLetterFrequencies(ciphertext)

    # detect missing letter
    gridPossible = 0 in letterFrequencies
    if gridPossible:
        lf = np.array(letterFrequencies)
        lettersWithZeroOccurences = (np.argsort(lf)[:letterFrequencies.count(0)])
        print("Doesn't contain:", intToString(lettersWithZeroOccurences))
    # ---------Testing statistics over periods----------

    # evalOverPeriods(ciphertext, evaluateLetterFrequenciesUnsubstituted)
    # evalOverPeriods(ciphertext, IOC)
    # evalOverPeriods(ciphertext, IOCTimesEntropy)
    # evalOverPeriods(ciphertext, evaluateBigramFrequencies) # Is this actually useful?
    # evalOverPeriods(ciphertext, evaluateQuadgramFrequencies)
    # for ciphers like playfair of bigram substitution, we need the block option for IOC - up to maybe 10?
    # English IOCs in non-overlapping blocks: monogram 0.067, bigram 0.008, trigram 0.0017
    print("Monogram IOC (English 0.067)", IOC(ciphertext))
    # !! unreliable for short lengths as usual.
    print("Bigram IOC (English 0.006-0.008) ", IOC(ciphertext, block=2)) # in playfair, a 2-letter ciphertext block is dependent on all 2 letters in a bigram
    print("Trigram IOC (English 0.0012-0.0016 (?))", IOC(ciphertext, block=3)) # in 3x3 Hill, dependent on all 3 letters in a trigram. I'm guessing the variance just comes from the randomness of the text - entropy?

if __name__ == "__main__":
    main()
    pass