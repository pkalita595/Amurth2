import numpy as np

def modConcate(a, b):
    a_l = a[:a.index(0)]
    b_l = b[:b.index(0)]
    a_l.extend(b_l)
    a_l.append(0)

    #print("modConcate", a, " ", b, " ", a_l)
    return a_l


def concatStrNOS(str1, str2):
    s1 = len(str1)
    s2 = len(str2)

    m = 5
    ans = []
    for l in range(1, s1):
        for k in range(1, s2):
            ans.append(modConcate(str1[l], str2[k]))

    return ans

def getStrSum(s):
    return sum(s[:s.index(0)])

def getStrType(s):
    if s <= 20:
        return 1
    else:
        if s <= 30:
            return 5
        else:
            return 2

def hasSpecialString(s):
    noSp = 1
    allSp = 1
    someSp = 0

    for l in range(1, len(s)):
        if s[l][0] != 0:
            if getStrType(getStrSum(s[l])) == 5:
                noSp = 0
            else:
                allSp = 0
                someSp = 1

    if allSp:
        return 1
    else:
        if noSp:
            return 0
        else:
            return 2


def strContainsNum(s):
    for l in range(1, len(s)):
        if s[l][0] != 0 and getStrType(getStrSum(s[l])) == 1:
            return True
    
    return False

def getNOfromSSK(ss):
    num = False
    oth = False
    
    for l in range(1, len(ss)):
        if ss[l][0] != 0:
            s = getStrSum(ss[l])
            t = getStrType(s)
            if t == 1:
                if oth:
                    return 3
                num = True
            else:
                if num:
                    return 3
                oth = True
    
    if num:
        return 1
    else:
        if oth:
            return 2
        else:
            return 0



def getNOSfromSSK(s):
    check = hasSpecialString(s)
    if check == 0:
        c = getNOfromSSK(s)
        if c == 1 or c == 0:
            return c
        elif c == 2:
            return 4
        elif c == 3:
            return 5
    elif check == 1:
        return 6
    elif strContainsNum(s):
        return 3
    else:
        return 2

def gammacheckNOS(arg1ssk, arg2ssk, cexs):
    print("NOS gammacheck 1: ", arg1ssk)
    print("NOS gammacheck 2: ", arg2ssk)
    print("NOS gammacheck cex: ", cexs)

    K = 4
    arg1 = [list(i) for i in np.array_split(arg1ssk, K)]  #[arg1ssk[idx::K] for idx in range(0, K)]
    arg2 = [list(i) for i in np.array_split(arg2ssk, K)]  #[arg2ssk[idx::K] for idx in range(0, K)]
    print("NOS gammacheck 1: ", arg1)
    print("NOS gammacheck 2: ", arg2)

    ss = concatStrNOS(arg1, arg2)
    output = getNOSfromSSK(ss)

    cex = getNOSfromSSK([[0,0,0], cexs, [0,0,0], [0,0,0], [0,0,0]])
    
    if (cex == 1 and output == 5) or (cex == 6 and output == 2) or (cex == 4 and output == 2) or (cex == 4 and output == 5):
        print("first case")
        return True
    elif (cex == 0 or output == 3):
        print("second case")
        return True
    else:
        print("third case")
        return output == cex


def gammaCheck(ls, cex):
    return gammacheckNOS(ls[0], ls[2], cex)

#def gammaCheck(absVal, cex):
#    print("getting called here")
#    return False

def getBeta(cex):
    return [[0,0,0,0,0,0,0,0,0,0,cex,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

def getBootstrap(N = 0, bootStrapParam = None):
    pos = {"SSK":[], "NOS":[]}
    neg = {"SSK":[], "NOS":[]}

    pos["SSK"].append([[0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],1, [0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],1, [1,1,1,2,2,2,0,0,0,0]])
    
    pos["NOS"].append([[0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],1, [0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0],1, [1,0,0,0,0,0,0,0,0,0]])
 
    #############################################
    #pos.append([[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,1,2,3,0,0,0,0,0,0,0,2,7,3,0,0,0,0,0,0,0], [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

    #pos.append([[0,0,0,0,0,0,0,0,0,0,8,1,6,0,0,0,0,0,0,0,2,4,6,0,0,0,0,0,0,0,7,3,1,0,0,0,0,0,0,0], [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

    #pos.append([[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,1,2,3,0,0,0,0,0,0,0,2,7,3,0,0,0,0,0,0,0], [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

    #pos.append([[0,0,0,0,0,0,0,0,0,0,8,1,6,0,0,0,0,0,0,0,2,4,6,0,0,0,0,0,0,0,7,3,1,0,0,0,0,0,0,0], [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])


    #pos.append([[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

    #pos.append([[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

    #neg.append([[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

    #neg.append([[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
    return pos, neg
