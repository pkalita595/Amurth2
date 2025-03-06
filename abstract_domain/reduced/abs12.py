import random 

def concreteFn(a):
    if a < 0:
        return -a
    else:
        return a

#Do not change the name of function, change the definition
def getBootstrap(N, opt = None):
    #pos = {"oddIntv": [], "evenIntv": []}
    #neg = {"oddIntv":[], "evenIntv":[]}

    pos = {"oddIntv": [[67, 75, 52, 78,  73], [-3, 3, -4, 8, 3], [ -9, 7, -4, 2, 2], [3, 5, 2, 6, 4], [-9, 7, -4, 2, 0], [-7, -3, -10, -2, 3],[-7, -3, -10, -2, 5]], "evenIntv": [[67, 75, 52, 78,  73], [-3, 3, -4, 8, 3], [ -9, 7, -4, 2, 2], [3, 5, 2, 6, 4], [-9, 7, -4, 2, 0], [-7, -3, -10, -2, 3],[-7, -3, -10, -2, 5]]}

    neg = {"oddIntv":[[67, 75, 52, 72, 75], [-3, 3, -4, 8, 6], [-7, -3, -10, -2, 2],[-7, -3, -10, -2, 0], [3,5,2,16,8], [-3, 3, -4, 8, -2]], "evenIntv":[[67, 75, 52, 72, 75], [-3, 3, -4, 8, 6], [-7, -3, -10, -2, 0],[-7, -3, -10, -2, 0], [3,5,2,16,8], [-3, 3, -4, 8, -2]]}

    return pos, neg

def concreteFun(a):
    if a < 0:
        return -a
    else:
        return a

def reduction(l1, r1, l2, r2):
    max1 = l1 if l1 > l2 else l2
    min1 = r1 if r1 < r2 else r2

    if max1 % 2 != 0:
        l2 = max1 - 1
    else:
        l1 = max1 - 1

    if min1 % 2 != 0:
        r2 = min1 + 1
    else:
        r1 = min1 + 1

    return l1, r1, l2, r2

def beta(low, high):
    oddLeft, oddRight, evenLeft, evenRight = 0, 0, 0, 0
    if low % 2 != 0:    # low is odd
        oddLeft = low
        evenLeft = low - 1
    else:
        oddLeft = low - 1
        evenLeft = low
    if high % 2 != 0:    # high is odd
        oddRight = high
        evenRight = high + 1
    else:
        oddRight = high + 1
        evenRight = high
    return oddLeft, oddRight, evenLeft, evenRight


'''
def gammaCheck(exList, cex):
    return False
    exList[0], exList[1], exList[2], exList[3] = reduction(exList[0], exList[1], exList[2], exList[3])
    
    lowO = concreteFun(exList[0])
    highO = concreteFun(exList[1])

    lowE = concreteFun(exList[2])
    highE = concreteFun(exList[3])
    return (lowO <= cex and cex <= highO) or (lowE <= cex and cex <= highE)

'''

def join(a, b):
    l1 = a[0]
    r1 = a[1]
    l2 = b[0]
    r2 = b[1]
    return [min(l1, l2), max(r1, r2)]

def gammaCheck(exList, cex):
    low = max(exList[0], exList[2])
    high = min(exList[1], exList[3])
    
    # low = concreteFun(low)
    # high = concreteFun(high)
    temp = [concreteFun(low), concreteFun(low)]
    for i in range(low + 1, high+1):
        temp = join([concreteFun(i), concreteFun(i)], list(temp))

    return temp[0] <= cex and cex <= temp[1]
