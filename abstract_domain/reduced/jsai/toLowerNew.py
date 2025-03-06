import numpy as np

#Do not change the name of function, change the definition
def modConcate(a, b):
    # print("a", a)
    # print("b", b)
    a_l = a[:a.index(0)]
    b_l = b[:b.index(0)]
    a_l.extend(b_l)
    a_l.append(0)

    #print("modConcate", a, " ", b, " ", a_l)
    return a_l

def isEqual(a, b):
    if a.index(0) != b.index(0):
        return False
    else:
        for i in range(len(a)):
            if a[i] != b[i]:
                return False
    return True

def getBeta(cex):
    return [cex]

def checkPos(ls, cex):
    if ls[0][0] == 2 or ls[1][0] == 2:
        if cex[0] == 2 and cex[1] == 0:
            return True
        else:
            return False
    if ls[0][0] == 1 or ls[1][0] == 1:
        if cex[0] == 1 and cex[1] == 0:
            return True
        else:
            return False

    con = modConcate(ls[0][1:], ls[1][1:])
    conVal = []
    conVal.append(ls[0][0] or ls[1][0])
    conVal.extend(con)
    if isEqual(conVal, cex):
        return True
    else:
        return False

def trim(st):
    temp = [i for i in st if i != 10]
    if len(temp) < 10:
        for i in range(len(temp) - 10):
            temp.append(0)
    return temp

def toUpper(st):
    temp = list(st)
    for i in range(len(st)):
        if (st[i] < 27) and (st[i] >= 20) and (st[i] != 0):
            temp[i] = st[i] + 7
    return temp


def toLower(st):
    temp = list(st)
    for i in range(len(st)):
        if st[i] >= 27 :
            temp[i] = st[i] - 7
    return temp

def gammaCheck(ls, cex):
    K = 2
    arg1 = [list(i) for i in np.array_split(ls[0], K)] 

    print("arg1: ", arg1)
    print("Cex: ", cex)

    res = []
    for i in range(1, K):
        for j in range(1, K):
            res.append(toLower(arg1[i]))    
            print("toLower", toLower(arg1[i]))
   
    for l in res:
        if isEqual(l, cex):
            return True

    if len(res) > K:
        return True    

    return False

def getBootstrap(N = 0, bootStrapParam = None):
    pos = {"SSK":[], "NOS":[]}
    neg = {"SSK":[], "NOS":[]}

    pos["SSK"].append([[0,0,0,0,0,0,0,0,0,0,15,16,30,0,0,0,0,0,0,0], 2, [15,16,23,0,0,0,0,0,0,0]])
    pos["NOS"].append([[0,0,0,0,0,0,0,0,0,0,15,16,30,0,0,0,0,0,0,0], 2, [15,16,23,0,0,0,0,0,0,0]])

    pos["NOS"].append([[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 6, [12,16,23,0,0,0,0,0,0,0]])
    pos["NOS"].append([[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 6, [12,16,0,0,0,0,0,0,0,0]])
    pos["NOS"].append([[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 4, [12,16,23,0,0,0,0,0,0,0]])
    # pos["NOS"].append([[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 1, [100,0,0,0,0,0,0,0,0,0]])
    pos["NOS"].append([[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 2, [12,10,10,0,0,0,0,0,0,0]])
    pos["NOS"].append([[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 2, [12,10,0,0,0,0,0,0,0,0]])

    neg["SSK"].append([[0,0,0,0,0,0,0,0,0,0,15,16,23,0,0,0,0,0,0,0], 2, [15,16,30,0,0,0,0,0,0,0]])
    neg["NOS"].append([[0,0,0,0,0,0,0,0,0,0,15,16,23,0,0,0,0,0,0,0], 2, [4,6,0,0,0,0,0,0,0,0]])    
    neg["NOS"].append([[0,0,0,0,0,0,0,0,0,0,15,16,23,0,0,0,0,0,0,0], 2, [14,8,0,0,0,0,0,0,0,0]])    

    return pos, neg
