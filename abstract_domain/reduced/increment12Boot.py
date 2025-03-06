import random 

def concreteFn(a):
    return a + 1 # increment

#Do not change the name of function, change the definition
def getBootstrap(N, opt = None):
    pos = {"oddIntv": [[67, 75, 52, 78,  73], [-3, 3, -4, 8, 4], [ -9, 7, -4, 2, 3], [3,5,2,6,4], [-3, 3, -4, 8, -2], [ -9, 7, -4, 2, 3], [-7, -3, -10, -2, -6],[-7, -3, -10, -2, -2],[59, 63, 58, 64, 60], [59, 63, 58, 64, 64], [77, 85, 78, 84, 79], [77, 85, 78, 84, 85], [-19, -9, -18, -8, -17], [-19, -9, -18, -8, -8], [15, 23, 14, 22, 16], [15, 23, 14, 22, 23], [-21, -13, -20, -14, -19], [-21, -13, -20, -14, -13], [-85, -79, -84, -78, -83], [-85, -79, -84, -78, -78], [29, 35, 28, 36, 30], [29, 35, 28, 36, 36], [-101, -95, -100, -94, -99], [-101, -95, -100, -94, -94], [-81, -75, -82, -74, -80], [-81, -75, -82, -74, -74], [95, 103, 94, 104, 96], [95, 103, 94, 104, 104]], "evenIntv": [[67, 75, 52, 78,  73], [-3, 3, -4, 8, 4], [ -9, 7, -4, 2, 3], [3,5,2,6,4], [-3, 3, -4, 8, -2], [ -9, 7, -4, 2, 3], [-7, -3, -10, -2, -6],[-7, -3, -10, -2, -2]]}
    neg = {"oddIntv":[[67, 75, 52, 72, 75], [-3, 3, -4, 8, 6], [-7, -3, -10, -2, -8],[-7, -3, -10, -2, 0], [3,5,2,16,8],[59, 63, 58, 64, 56], [59, 63, 58, 64, 68], [77, 85, 78, 84, 73], [77, 85, 78, 84, 91], [-19, -9, -18, -8, -26], [-19, -9, -18, -8, 1], [15, 23, 14, 22, 9], [15, 23, 14, 22, 30], [-21, -13, -20, -14, -25], [-21, -13, -20, -14, -7], [-85, -79, -84, -78, -88], [-85, -79, -84, -78, -73], [29, 35, 28, 36, 24], [29, 35, 28, 36, 42], [-101, -95, -100, -94, -104], [-101, -95, -100, -94, -89], [-81, -75, -82, -74, -86], [-81, -75, -82, -74, -68], [95, 103, 94, 104, 88], [95, 103, 94, 104, 112]], "evenIntv":[[67, 75, 52, 72, 75], [-3, 3, -4, 8, 6], [-7, -3, -10, -2, -8],[-7, -3, -10, -2, 0], [3,5,2,16,8]]}
    return pos, neg

def concreteFun(a):
    return a + 1

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

def gammaCheck(exList, cex):
    low = max(exList[0], exList[2])
    high = min(exList[1], exList[3])
    low = concreteFun(low)
    high = concreteFun(high)
    # oddLeft, oddRight, evenLeft, evenRight = beta(low, high)
    # low = max(oddLeft, evenLeft)
    # high = min(oddRight, evenRight)
    return low <= cex and cex <= high
