import random 
#Do not change the name of function, change the definition
def getBootstrap(N, opt = None):
    pos, neg = [], []
    pos = [[67, 75, 52, 78,  73], [-3, 3, -4, 8, 4], [ -9, 7, -4, 2, 3], [3,5,2,6,4], [-3, 3, -4, 8, -2], [ -9, 7, -4, 2, 3], [-7, -3, -10, -2, -6],[-7, -3, -10, -2, -2]]
    neg = {"oddIntv":[[67, 75, 52, 72, 74], [-3, 3, -4, 8, 6], [-7, -3, -10, -2, -8],[-7, -3, -10, -2, 0]], "evenIntv":[[67, 75, 52, 72, 74], [-3, 3, -4, 8, 6], [-7, -3, -10, -2, -8],[-7, -3, -10, -2, 0]]}
    return pos, neg

def concreteFun(a):
    return a + 1

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

def gammaCheck(exList, cex):
    low = max(exList[0], exList[2])
    high = min(exList[1], exList[3])
    low = concreteFun(low)
    high = concreteFun(high)
    # oddLeft, oddRight, evenLeft, evenRight = beta(low, high)
    # low = max(oddLeft, evenLeft)
    # high = min(oddRight, evenRight)
    return low <= cex and cex <= high
