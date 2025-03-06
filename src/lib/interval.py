import ctypes
import ctypes.util
# call f_c
import itertools

import lib.utility as util
from py_console import console

def getFC(config, inputList):
    func = config["tosynthesize"].keys()
    proto = config["tosynthesize"][func[0]]
    toolPath = config["basepath"]
    tosynthesize = func[0]

    if config["extlib"] == "":
        libPath = ctypes.util.find_library("c")
        lib = ctypes.cdll.LoadLibrary(libPath)
    else:
        lib = ctypes.CDLL(toolPath + "external_lib/" + config["extlib"])

    if "int" in proto[0]:
        if "*" in proto[0]:
            lib[tosynthesize].restype = ctypes.POINTER(ctypes.c_int)
        lib[tosynthesize].restype = ctypes.c_int
    args = []
    for i in proto[1:]:
        if "int" in i:
            if "*" in i:
                args.append(ctypes.POINTER(ctypes.c_int))
            args.append(ctypes.c_int)

    lib[tosynthesize].argtypes = args
    if type(inputList) != list:
        ret = lib[tosynthesize](inputList)
    else:
        ret = lib[tosynthesize](*inputList)

    return ret


# Checks whether cex is in \gamma(absVal)
def gammaCheck(config, absVal, cex):
    tempPath = config["basename"] + "/temp/"
    lib = ctypes.CDLL(tempPath + "domain.so")
    absVal.append(cex)
    return lib['GammaCheck'](*absVal)


# \beta: representaion function
def betaOp(config, cex):
    tempPath = config["basepath"] + "/temp/"
    # call beta function
    lib = ctypes.CDLL(tempPath + "domain.so")
    if "int" in config["abstract_value"][0][1][0]:
        absVal = (ctypes.c_int * len(config["abstract_value"]))()
        lib['Beta'].argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
    lib['Beta'](cex, absVal)

    absList = [i for i in absVal]

    return absList


# get concrete set of an abstract value
def gammaOp(config, absVal):
    tempPath = config["basename"] + "/temp/"
    args = []
    absValTmp = absVal[:]
    lib = ctypes.CDLL(tempPath + "domain.so")
    if "int" in config["abstract_value"][0][1][0]:
        for i in config["abstract_value"]:
            args.append(ctypes.c_int)
        args.append(ctypes.POINTER(ctypes.c_int))

    lib['Gamma'].argtypes = args
    lib['Gamma'].restype = ctypes.c_int
    output = (ctypes.c_int * 400)()
    absValTmp.append(output)
    size = lib['Gamma'](*absValTmp)

    conc = []
    for i in range(size):
        conc.append(output[i])

    return conc


def joinOp(config, in1, in2):
    tempPath = config["basename"] + "/temp/"
    args = []
    funArgs = []
    lib = ctypes.CDLL(tempPath + "domain.so")
    if len(config["abstract_value"]) == 1:
        if "int" in config["abstract_value"][0][1][0]:
            for i in range(2):
                args.append(ctypes.c_int)
            args.append(ctypes.POINTER(ctypes.c_int))
        funArgs.append(in1)
        funArgs.append(in2)

    else:
        if "int" in config["abstract_value"][0][1][0]:
            for i in range(3):
                args.append(ctypes.POINTER(ctypes.c_int))
        funArgs.extend(in1)
        funArgs.extend(in2)

    out = (ctypes.c_int * len(config["abstract_value"]))()

    funArgs.append(out)

    lib["Join"](*funArgs)

    return [i for i in out]


# calculate \hat(f_#)
def fSharpHat(config, absVec):
    func = list(config["tosynthesize"].keys())
    tosynthesizeProto = config["tosynthesize"][func[0]]
    toolPath = config["basepath"]
    tosynthesize = func[0]

    tempAbsVec = absVec[:]
    gammaValTemp = []
    for i in range(len(tosynthesizeProto) - 1):
        temp = []
        for j in range(len(config["abstract_value"])):
            temp.append(tempAbsVec.pop(0))

        gammaValTemp.append(gammaOp(config, temp))

    gammaLists = []
    for element in itertools.product(*gammaValTemp):
        gammaLists.append(list(element))
    joinVal = betaOp(config, getFC(config, gammaLists[0]))
    for i in range(1, len(gammaLists)):
        joinVal = joinOp(config, betaOp(config, getFC(config, gammaLists[i])), joinVal)

    print("Before sending in fSharpHat", joinVal)
    return joinVal


# gamma in python
def checkPosOrNeg(config, exList, cex, domainPy):

    res = False
    toolPath = config["basepath"]
    tempPath = toolPath + "/temp/"

    res = domainPy.gammaCheck(exList, cex)
    console.warn("Inside checkPosOrNeg: <exList, cex>, res", exList, cex, res)
    return res
