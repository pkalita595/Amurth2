import random 

def concreteFn(a, b):
    return a - b # addition


#Do not change the name of function, change the definition
def check_pos(ex):
    l1 = ex[0]
    u1 = ex[1]
    l2 = ex[2]
    u2 = ex[3]
    c = ex[4]
    ls = []
    for i in range(l1, u1+1):
        for j in range(l2, u2+1):
            ls.append(abs(i) + abs(j))
    ls.sort()
    if c in ls:
        return True, [l1, u1, l2, u2, ls[0], ls[-1]]
    else:
        return False, [l1, u1, l2, u2, c, c]


def concreteFunction(a, b):
    return a - b

def gammaCheck(exList, cex):
    low1 = max(exList[0], exList[2])
    high1 = min(exList[1], exList[3])
    low2 = max(exList[4], exList[6])
    high2 = min(exList[5], exList[7])
    low = concreteFunction(low2, low1)
    high = concreteFunction(high2, high1)

    return low <= cex and cex <= high


def getBootstrap(N, opt = None):
    return [], []
    # return [], {"oddIntv":[], "evenIntv":[]}
    # pos = [[3, 7, 2, 4, 1, 3, 2, 4, 5, 7, 4, 8], [1, 3, 2, 4,3, 7, 2, 4, 4, 5, 7, 4, 8], [-3, 5, -10, 6, -11, 5, -6, 4, -9, 9, -10, 10], [-11, 5, -6, 4, -3, 5, -10, 6, -9, 9, -10, 10]]
    pos = [[3, 7, 2, 4, 1, 3, 2, 4, 5],[3, 7, 2, 4, 1, 3, 2, 4, 7], [1, 3, 2, 4,3, 7, 2, 4, 7],
           [1, 3, 2, 4,3, 7, 2, 4, 5], [-3, 5, -10, 6, -11, 5, -6, 4, 9], [-3, 5, -10, 6, -11, 5, -6, 4, -9],
           [-11, 5, -6, 4, -3, 5, -10, 6, -9],[-11, 5, -6, 4, -3, 5, -10, 6, 9]]
    # [[3, 7, 2, 4, 1, 3, 2, 4, 4], [3, 7, 2, 4, 1, 3, 2, 4, 8], [1, 3, 2, 4, 3, 7, 2, 4, 8],
     # [1, 3, 2, 4, 3, 7, 2, 4, 4], [-3, 5, -10, 6, -11, 5, -6, 4, 10], [-3, 5, -10, 6, -11, 5, -6, 4, -8],
     # [-11, 5, -6, 4, -3, 5, -10, 6, -8], [-11, 5, -6, 4, -3, 5, -10, 6, 10]]
    neg = {"oddIntv":[[3, 7, 2, 4, 1, 3, 2, 4, 4], [3, 7, 2, 4, 1, 3, 2, 4, 8], [1, 3, 2, 4, 3, 7, 2, 4, 8],
     [1, 3, 2, 4, 3, 7, 2, 4, 4], [-3, 5, -10, 6, -11, 5, -6, 4, 10], [-3, 5, -10, 6, -11, 5, -6, 4, -10],
     [-11, 5, -6, 4, -3, 5, -10, 6, -10], [-11, 5, -6, 4, -3, 5, -10, 6, 10]],
     "evenIntv":[[3, 7, 2, 4, 1, 3, 2, 4, 3],
     [3, 7, 2, 4, 1, 3, 2, 4, 9], [1, 3, 2, 4, 3, 7, 2, 4, 9], [1, 3, 2, 4, 3, 7, 2, 4, 3],
     [-3, 5, -10, 6, -11, 5, -6, 4, 11], [-3, 5, -10, 6, -11, 5, -6, 4, -11],
     [-11, 5, -6, 4, -3, 5, -10, 6, -11], [-11, 5, -6, 4, -3, 5, -10, 6, 11]]} # [[67, 75, 51, 61, 118, 136], [67, 75, 51, 61, 118, 137], [67, 75, 51, 61, 117, 136], [87, 93, -91, -87, -4, 6], [87, 93, -91, -87, -4, 7], [87, 93, -91, -87, -5, 6]]
    return pos, neg

    for i in range(N):
        l1 = random.randint(-100, 100)
        d1 = random.randint(4, 10)
        u1 = l1 + d1
        l2 = random.randint(-100, 100)
        d2 = random.randint(4, 10)
        u2 = l2 + d2
        S1 = random.sample(range(l1, u1+1), d1+1)
        S2 = random.sample(range(l2, u2+1), d2+1)

        a_ap = [(x) + (y) for x in S1 for y in S2]
        a_ap.sort()
        d = max(d1, d2)
        #positive example
        pos.append([l1, u1, l2, u2, a_ap[0], a_ap[-1]])

        #left negative example
        neg.append([l1, u1, l2, u2, a_ap[0] - d, a_ap[0] - d])
        #right negative example
        neg.append([l1, u1, l2, u2, a_ap[-1] + d, a_ap[-1] + d])

    return pos, neg

'''
a, b = getBootstrap(5)
print a
print b
'''
