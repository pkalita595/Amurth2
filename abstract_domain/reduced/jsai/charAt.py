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

def gammaCheck(ls, cex):
    print("In checkPos.domainPy.py")
    print(ls)
    print(cex)
    print("~~~~")
    K = 2
    arg1 = [list(i) for i in np.array_split(ls[0], K)] 
    idx = int(ls[2].strip().replace(')','').split('=')[-1])

    print("arg1: ", arg1)
    print("idx: ", idx)
    print("Cex: ", cex)

    for i in range(1, K):
        if arg1[i].index(0) <= idx: 
            print("GOT HERE")
            continue
        elif arg1[i][idx] == cex[0] and cex[1] == 0:
            return True
   
    return False

def getBootstrap(N = 0, bootStrapParam = None):
    pos = {"SSK":[], "NOS":[]}
    neg = {"SSK":[], "NOS":[]}

    pos["SSK"].append([[0,0,0,0,0,0,0,0,0,0,1,4,3,1,0,0,0,0,0,0],1, "new intCP(isTop = 0, isBot = 0, value = 2)", [3,0,0,0,0,0,0,0,0,0]])
    pos["NOS"].append([[0,0,0,0,0,0,0,0,0,0,1,4,3,1,0,0,0,0,0,0],1,"new intCP(isTop = 0, isBot = 0, value = 2)", [3,0,0,0,0,0,0,0,0,0]])

    pos["SSK"].append([[0,0,0,0,0,0,0,0,0,0,11,4,3,1,0,0,0,0,0,0],2,"new intCP(isTop = 0, isBot = 0, value = 3)", [1,0,0,0,0,0,0,0,0,0]])
    pos["NOS"].append([[0,0,0,0,0,0,0,0,0,0,11,4,3,1,0,0,0,0,0,0],2,"new intCP(isTop = 0, isBot = 0, value = 3)", [1,0,0,0,0,0,0,0,0,0]])

    return pos, neg
