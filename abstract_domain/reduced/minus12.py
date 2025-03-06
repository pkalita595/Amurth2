import random 

def concreteFn(a, b):
    return a - b # subtraction


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
    return a+b

def gammaCheck(exList, cex):
    low1 = max(exList[0], exList[2])
    high1 = min(exList[1], exList[3])
    low2 = max(exList[4], exList[6])
    high2 = min(exList[5], exList[7])
    a = []
    a.append(concreteFunction(low2, low1))
    a.append(concreteFunction(high2, high1))

    a.sort()
    low = a[0]
    high = a[1]

    return low <= cex and cex <= high


def getBootstrap(N, opt = None):
    pos = {"oddIntv":[[17, 27, 16, 28, -7, 1, -6, 2, 16], [17, 27, 16, 28, -7, 1, -6, 2, 33], [-91, -81, -92, -82, -87, -79, -88, -80, -11], [-91, -81, -92, -82, -87, -79, -88, -80, 5], [95, 105, 96, 106, 9, 19, 10, 20, 77], [95, 105, 96, 106, 9, 19, 10, 20, 95], [-61, -53, -60, -54, 81, 89, 80, 90, -149], [-61, -53, -60, -54, 81, 89, 80, 90, -135], [87, 91, 86, 92, 31, 41, 30, 40, 47], [87, 91, 86, 92, 31, 41, 30, 40, 60]], "evenIntv" : [[17, 27, 16, 28, -7, 1, -6, 2, 16], [17, 27, 16, 28, -7, 1, -6, 2, 33], [-91, -81, -92, -82, -87, -79, -88, -80, -11], [-91, -81, -92, -82, -87, -79, -88, -80, 5], [95, 105, 96, 106, 9, 19, 10, 20, 77], [95, 105, 96, 106, 9, 19, 10, 20, 95], [-61, -53, -60, -54, 81, 89, 80, 90, -149], [-61, -53, -60, -54, 81, 89, 80, 90, -135], [87, 91, 86, 92, 31, 41, 30, 40, 47], [87, 91, 86, 92, 31, 41, 30, 40, 60]]}

    neg = {"oddIntv":[ [67, 75, 66, 76, -31, -23, -30, -22, 107], [17, 27, 16, 28, -7, 1, -6, 2, 14], [17, 27, 16, 28, -7, 1, -6, 2, 35], [-91, -81, -92, -82, -87, -79, -88, -80, -13], [-91, -81, -92, -82, -87, -79, -88, -80, 7], [95, 105, 96, 106, 9, 19, 10, 20, 75], [95, 105, 96, 106, 9, 19, 10, 20, 97], [-61, -53, -60, -54, 81, 89, 80, 90, -151], [-61, -53, -60, -54, 81, 89, 80, 90, -133], [87, 91, 86, 92, 31, 41, 30, 40, 45], [87, 91, 86, 92, 31, 41, 30, 40, 62]], "evenIntv":[ [67, 75, 66, 76, -31, -23, -30, -22, 107], [17, 27, 16, 28, -7, 1, -6, 2, 14], [17, 27, 16, 28, -7, 1, -6, 2, 35], [-91, -81, -92, -82, -87, -79, -88, -80, -13], [-91, -81, -92, -82, -87, -79, -88, -80, 7], [95, 105, 96, 106, 9, 19, 10, 20, 75], [95, 105, 96, 106, 9, 19, 10, 20, 97], [-61, -53, -60, -54, 81, 89, 80, 90, -151], [-61, -53, -60, -54, 81, 89, 80, 90, -133], [87, 91, 86, 92, 31, 41, 30, 40, 45], [87, 91, 86, 92, 31, 41, 30, 40, 62]]}


    return pos, neg


