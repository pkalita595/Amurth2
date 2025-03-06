import importlib
import os
import re
import sys
import xml.etree.ElementTree as ET

import lib.interval as intv
import lib.utility as util
from py_console import console



# This function creates the sketch file for synthesis
# cexGenFlag is to determine whether to generate cex or not
# maxsatFlag is to determine whether to dump MAXSAT constraints or not
# dumpSketchFile(config, skfile, generator, gammaCheck, gammaCheck_c, aux_func, culprit, curNex)
# config, skfile, generator, aux_func, culprit, domainList, curNex
def dumpSketchFile(config, skfile, generator, aux_func, culpritDomainName, domainMap, curNex, posex, cexGenFlag, maxsatFlag):
    # culpritDomainName = []

    culpritFun = []
    if type(culpritDomainName) == str:
        culpritFun = domainMap[culpritDomainName]
        culpritDomainName = [culpritDomainName]
    elif type(culpritDomainName) == list:
        for i in culpritDomainName:
            culpritFun.extend(domainMap[i])

    domainMapNew = {}
    for info in config["domains"]:
        domainMapNew[info[0]] = info[1]

    toolPath = config["basepath"]
    tempPath = toolPath + "/temp/"

    util.emit(generator, skfile)
    util.emit(aux_func, skfile)
    util.emit_file(toolPath + "abstract_domain/" + config["abstract_domain"][0], skfile)
    # now dump based on the culprit domain
    # as culprit will have generator and
    # \mathcal{D} \setminus culprit will have synthesized functions

    util.emit(["\n//synthesized functions\n"], skfile)
    dumpCulpritTransformer(skfile, culpritFun, domainMapNew, tempPath)

    util.emit(["\n//gammaCheck_c\n"], skfile)

    gammaCheck_c = getGammaCheck_c(config, domainMapNew)
    util.emit(gammaCheck_c, skfile)

    util.emit(["harness void main(){\n"], skfile)

    func = list(config["tosynthesize"].keys())
    proto = config["tosynthesize"][func[0]]  # getting the prototype of the concrete operator

    inputLen = len(proto) - 1

    absValue = config["abstract_value"]
    arrayFlag = 0
    if re.search("\[.*\]", proto[0]) and arrayFlag == 0:
        arrayFlag = 1

    concreteFn = list(config["tosynthesize"])[0]
    if "contains" in  concreteFn:
        arrayFlag = 1

    if cexGenFlag == 1:

        if arrayFlag == 0:
            dumpHole(config, skfile, proto, inputLen)
        else:
            dumpHoleArray(config, skfile, proto, inputLen)

        # counterexample generation

        # getting all input parameter
        absValstr = ""
        valList = []
        if len(set(proto[1:])) != 1:
            if config["string_domain"][0] == "charIn":
                # hatao
                absValstr = "MustSet1, MaySet1, absFlag1, intVal, "
            elif config["string_domain"][0] == "constStr":
                absValstr = "aStr1, intVal, "
            else:
                for i in range(len(absValue)):
                    absValstr += absValue[i][0] + "1, "
                absValstr += " intVal"
        else:
            valList = []
            for j in range(1, inputLen + 1):
                for i in range(len(absValue)):
                    valList.append(absValue[i][0] + str(j))
                    absValstr = ','.join([ele for ele in valList])

        
        cons = []
        cons_c = []
        print(culpritDomainName, len(culpritDomainName))
        assert (len(culpritDomainName) == 1)
        bitFlag = []
        for dom in culpritDomainName:
            if False:
                tcex = []
                tcex_c = []
                for ele in culpritFun:
                    tcex.append(str(ele) + '(' + absValstr + ')')
                    tcex_c.append(str(ele) + '_c(' + absValstr + ')')
                cons.append("GammaCheck" + dom + '(' + ','.join([elem for elem in tcex]) + ', cex)')
                cons_c.append("GammaCheck" + dom + '_c(' + ','.join([elem for elem in tcex_c]) + ', cex)')
            else:
                cons.append("GammaCheck" + dom + '(' + absValstr + ', cex)')
                cons_c.append("GammaCheck" + dom + '_c(' + absValstr + ', cex)')


        util.emit(["\t//SAT^- for h^_Li\n"], skfile)
        util.emit(["\tassert " + '&'.join('~(' + elem + ')' for elem in cons) + ';\n'], skfile)

        cons_c_other = ""
        
        for dname in domainMapNew.keys():
            util.emit(["\tbit " + dname + "_fe = " + "GammaCheck" + dname + '_c(' + absValstr + ', cex);\n'],skfile)
            bitFlag.append(dname + "_fe")

        allDom = []
        for dname in domainMap.keys():
            allDom.append(dname + "_fe")

        dnf = []
        for i in allDom:
            temp = []
            temp.append('~'+i)
            for j in allDom:
                if i == j:
                    continue
                temp.append(j)
            dnf.append(' & '.join([ele for ele in temp]))

        util.emit(['\tassert ' + ' & '.join([ele for ele in bitFlag]) + ';\n'], skfile) # earlier


        # should iterate for each argument of F_c

        for j in range(1, inputLen + 1):
            betaValstr = ""
            for i in range(len(absValue)):
                betaValstr += absValue[i][0] + str(j) + ", "
            # for dname in domainMap.keys():
            util.emit(["\tassert domainOpt" +"(" + betaValstr[:-2] + ");\n"], skfile)

            # one domain opt for mixed domains
            if len(set(proto[1:])) != 1:
                break

        if arrayFlag == 1:
            if re.search("\[.*\]", proto[0]):
                util.emit(["\tcreateString(cex, ??);\n"], skfile)
        else:
            util.emit(["\tcexOptimization(cex);\n"], skfile)  # sometime we have to do optimization on cex also

        func = func[0]
        if func == "lshl" or func == "lshr" or func == "ashr":
            util.emit(["\tassert (left2 == right2) && (left2 >= 0);\n"], skfile)

    if maxsatFlag == 1:
        util.emit(["\n\tint nCount = 0;\n\t//maxsat holes\n "], skfile)

        # add the maxsat flag holes
        if curNex:
            for i in curNex.keys():
                if "boot" not in i:
                    util.emit(["\tint %s = ??;\n" % i], skfile)

    util.emit(["\t//adding pos and neg examples\n"], skfile)
    # add pos/neg cex
    addCex(config, skfile, curNex, posex, maxsatFlag, proto, culpritDomainName, culpritFun)

    if maxsatFlag == 1:
        skfile.writelines(["\n\tminimize(nCount);\n"])

    skfile.writelines(["\n} //end of main\n"])


# return the line number where lookup (hole variable) is present in sketchFile
def getLineNo(sketchFile, lookup):
    for num, line in enumerate(open(sketchFile), 1):
        if lookup in line:
            return num
    return -1

# process the paramaeters from the hole.xml file for array
def processParamsArray(config, proto, sketchFile, holeMap, domainPy):
    absValue = config["abstract_value"]
    cexList = []

    concreteFn = list(config["tosynthesize"])[0]
    inputLen = len(proto) - 1

    if len(set(proto[1:])) != 1:
        stringDom = config["string_domain"]
        for j in range(1, inputLen + 1):
            if isInputArray(proto[j]):
                if stringDom == "safe" or stringDom == "jsai":
                    for i in range(len(absValue)):
                        valueLine = getLineNo(sketchFile, absValue[i][1][0] + " " + absValue[i][0] + str(j))
                        value = holeMap[valueLine]
                        cexList.append(value)
                        print("cexList: ", cexList)

                elif stringDom[0] == "charIn" or stringDom[0] == "pre_suf":
                    for i in range(1, len(stringDom)):
                        valueLine = getLineNo(sketchFile, "int[2*N] " + stringDom[i] + str(j))
                        value = holeMap[valueLine]
                        cexList.append(value)
                elif stringDom[0] == "constStr":
                    for i in range(1, len(stringDom)):
                        valueLine = getLineNo(sketchFile, "int[N+1] " + stringDom[i] + str(j))
                        value = holeMap[valueLine]
                        cexList.append(value)
                elif stringDom[0] == "hash":
                    for i in range(1, len(stringDom)):
                        valueLine = getLineNo(sketchFile, "int " + stringDom[i] + str(j))
                        value = holeMap[valueLine]
                        cexList.append(value)

                elif stringDom[0] == "ssk":
                    for i in range(1, len(stringDom)):
                        valueLine = getLineNo(sketchFile, "int[2*N][K+1] " + stringDom[i] + str(j))
                        value = holeMap[valueLine]
                        cexList.append(value)
            elif proto[j] == "int":
                if concreteFn == "charAt":
                    intVal = []
                    intVal.append(holeMap[getLineNo(sketchFile, "intVal.isTop")])
                    intVal.append(holeMap[getLineNo(sketchFile, "intVal.isBot")])
                    intVal.append(holeMap[getLineNo(sketchFile, "intVal.value")])
                    intValStr = "new intCP(isTop = " + str(intVal[0]) + ", isBot = " + str(intVal[1]) + ", value = " + str(
                        intVal[2]) + ")"
                    cexList.append(intValStr)

        ######################################################
    else:
        for j in range(1, inputLen + 1):
            for i in range(len(absValue)):
                valueLine = getLineNo(sketchFile, absValue[i][1][0] + " " + absValue[i][0] + str(j))
                value = holeMap[valueLine]
                cexList.append(value)

    # cex hole value
    cexLine = getLineNo(sketchFile, proto[0] + " cex =")
    cex = holeMap[cexLine]

    sys.path.insert(0, config["basepath"] + "/temp/")
    #use technique to import dynamically
    domainPy = importlib.import_module("domainPy")

    res = domainPy.gammaCheck(cexList, cex)
    cexList.append(cex)
    # print("res and cexList", res, cexList)
    return res, cexList


# it reads the hole values and assigns correct values to the corresponding holes and return whether cex is positive or negative example
def processParams(config, sketchFile, holeMap, domainPy):
    cexList = []
    absValue = config["abstract_value"]

    func = list(config["tosynthesize"].keys())
    proto = config["tosynthesize"][func[0]]
    inputLen = len(proto) - 1

    for j in range(1, inputLen + 1):
        for i in range(len(absValue)):
            signLine = getLineNo(sketchFile, "int " + absValue[i][0] + "sign" + str(j))
            if signLine == -1:
                console.error("Got -1 from getLineNo for " + absValue[i][0])
            signval = int(holeMap[signLine])
            valLine = getLineNo(sketchFile, "int " + absValue[i][0] + "val" + str(j))
            value = int(holeMap[valLine])
            cexList.append(value if signval == 0 else -value)

    # now add the cex hole value
    signLineCex = getLineNo(sketchFile, "int cexsign")
    signvalCex = int(holeMap[signLineCex])
    valLineCex = getLineNo(sketchFile, "int cexval")
    value = int(holeMap[valLineCex])
    ceX = value if signvalCex == 0 else -value

    res = intv.checkPosOrNeg(config, cexList, ceX, domainPy)
    cexList.append(ceX)

    return res, cexList

#returns hole map for holes without array
def getHoleMap(rootXml):
    holeMap = {}
    for child in rootXml:
        holeMap[int(child.attrib['line'])] = int(child.attrib['value'])

    return holeMap


#returns hole map in case of array
def getHoleMapArray(rootXml):
    holeMap = {}
    for child in rootXml:
        if(child.attrib['type'] == "array"):
            holeMap[int(child.attrib['line'])] = []
            for i in child:
                holeMap[int(child.attrib['line'])].append(int(i.attrib['value']))
        else:
            holeMap[int(child.attrib['line'])] = int(child.attrib['value'])
    return holeMap

def getLabel(label):
    temp = label.split('=')
    temp = temp[0].replace("int", "").strip()
    return temp

# process the holes generated by sketch
# labelCnt is the label counter to make holes for neg example
# make maxsatFlag 1 iff, there is no precision check
def processHoles(config, sketchFile, holeFile, maxsatFlag, logFile ,cexMap, negexSubset, dname, domainMap, domainPy, cexCnt):
    arrayFlag = 0
    func = list(config["tosynthesize"].keys())
    proto = config["tosynthesize"][func[0]]
    if re.search("\[.*\]", proto[0]):
        arrayFlag = 1

    labelCnt = len(negexSubset)
    tree = ET.parse(holeFile)
    root = tree.getroot()

    concreteFn = list(config["tosynthesize"])[0]
    if "contains" in concreteFn:
        arrayFlag = 1

    if arrayFlag == 0:
        # stores the hole mapping from line number to its value
        holeMap = getHoleMap(root)
    else:
        # stores the hole mapping from line number to a list of value for array
        holeMap = getHoleMapArray(root)

    mapex = {}
    res = 0
    if maxsatFlag == 0:
        if arrayFlag == 0:
            res, exmp = processParams(config, sketchFile, holeMap, domainPy)
        else:
            res, exmp = processParamsArray(config, proto, sketchFile, holeMap, domainPy)

    
        cexCnt += 1
        labelName = 'n%s' % cexCnt

        console.error("CexCnt: ", str(cexCnt), labelName, res)

        # cexCnt += 1
        if res == False:
            for i in domainMap.keys():
                cexMap["Negative"][i][labelName] = exmp
        else:
            for i in domainMap.keys():
                cexMap["Positive"][i][labelName] = exmp

        mapex[labelName] = exmp
        # return mapex, res

    if maxsatFlag <= 1:
        # now find the line number of holes and store in the map
        lookup = "maxsat holes"
        file_name = open(sketchFile)

        with open(sketchFile) as f:
            wholeFile = f.readlines()

        maxsatHole = 0
        for num, line in enumerate(file_name, 1):
            if lookup in line:
                maxsatHole = num
        maxsatHole += 1

        labelToRemove = []
        for i in range(labelCnt):
            try:
                if holeMap[maxsatHole + i] != 0:  # if maxsat drops it then make it as positive cex
                    label = getLabel(wholeFile[maxsatHole + i - 1])
                    labelToRemove.append(label)
            except:
                continue

        if len(labelToRemove) > 0:
            console.warn("Dropped in MAXSAT: {}".format(str(labelToRemove)))
        delta = {}
        # to pop the stored label which are to be pos cex
        for i in labelToRemove:
            delta[i] = cexMap["Negative"][dname][i]
            console.warn("Dropped neg ex: " + str(cexMap["Negative"][dname][i]))
            with open(logFile, 'a') as f:
                f.write("Dropped neg ex: " + str(cexMap["Negative"][dname][i]) + "\n")

            if i in cexMap["Positive"]:
                console.error("negative example is also in the positive example (label actually): may be due to the other domain")

            del cexMap["Negative"][dname][i]

        if maxsatFlag == 1:
            return delta, False, cexCnt
        else:
            return mapex, res, cexCnt

# following function to dump the hole in the sketch file
def dumpHole(config, skfile, proto, inputLen):
    absValue = config["abstract_value"]
    for j in range(1, inputLen + 1):
        for i in range(len(absValue)):
            util.emit(["\tint " + absValue[i][0] + "sign" + str(j) + "= ??;\n"], skfile)
            util.emit(["\tint " + absValue[i][0] + "val" + str(j) + "= ??;\n"], skfile)

    util.emit(["\tint cexsign = ??;\n"], skfile)
    util.emit(["\tint cexval = ??;\n"], skfile)

    for j in range(1, inputLen + 1):
        for i in range(len(absValue)):
            util.emit(["\tint " + absValue[i][0] + str(j) + " = (" + absValue[i][0] + "sign" + str(j) + "== 0 ? " +
                       absValue[i][0] + "val" + str(j) + " : -" + absValue[i][0] + "val" + str(j) + ");\n"], skfile)

    util.emit(["\tint cex = (cexsign == 0 ? cexval : -cexval);\n"], skfile)

    # adding precondtion based on the type of the abstract values
    for j in range(1, inputLen + 1):
        for i in range(len(absValue)):
            if absValue[i][1][0] == "intP":
                util.emit(["\tassert " + absValue[i][0] + str(j) + " > 0;\n"], skfile)
            if absValue[i][1][0] == "intN":
                util.emit(["\tassert " + absValue[i][0] + str(j) + " < 0;\n"], skfile)


# returns true if argument is an array datatype
def isInputArray(arg):
    return re.search("\[.*\]", arg)


# following function to dump the hole in the sketch file in presence of Array
def dumpHoleArray(config, skfile, proto, inputLen):
    concreteFn = list(config["tosynthesize"])[0]
    absValue = config["abstract_value"]
    if len(set(proto[1:])) != 1:
        stringDom = config["string_domain"]
        for j in range(1, inputLen + 1):
            if isInputArray(proto[j]):
                if stringDom == "safe" or stringDom == "jsai":
                    util.emit(["\t" + config["abstract_value"][0][1][0] + " " + config["abstract_value"][0][0] +
                               str(j) + " = ??;\n"], skfile)
                    util.emit(["\t" + config["abstract_value"][1][1][0] + " " + config["abstract_value"][1][0] + 
                               str(j) + " = ??;\n"], skfile)
                elif stringDom[0] == "charIn" or stringDom[0] == "pre_suf":
                    for i in range(1, len(stringDom)):
                        util.emit(["\t" + "int[2*N] " + stringDom[i] + str(j) + " = ??;\n"], skfile)
                elif "constStr" in stringDom[0]:
                    for i in range(1, len(stringDom)):
                        util.emit(["\t" + "int[N+1] " + stringDom[i] + str(j) + " = ??;\n"], skfile)
                elif "ssk" in stringDom[0] :
                    for i in range(1, len(stringDom)):
                        util.emit(["\t" + "int[2*N][K+1] " + stringDom[i] + str(j) + " = ??;\n"], skfile)
                elif "hash" in stringDom[0]:
                    for i in range(1, len(stringDom)):
                        util.emit(["\t" + "int " + stringDom[i] + str(j) + " = ??;\n"], skfile)
            elif proto[j] == "int":
                if concreteFn == "charAt":
                    util.emit(["\tintCP intVal = new intCP();\n"], skfile)
                    util.emit(["\tintVal.isTop = ??;\n"], skfile)
                    util.emit(["\tintVal.isBot = ??;\n"], skfile)
                    util.emit(["\tintVal.value = ??;\n"], skfile)
    else:
        for j in range(1, inputLen + 1):
            for i in range(len(absValue)):
                util.emit(["\t" + absValue[i][1][0] + " " + absValue[i][0] + str(j) + " = ??;\n"], skfile)

    util.emit(["\t" + proto[0] + " cex = ??;\n"], skfile)


def createGenFiles(config):
    toolPath = config["basepath"]
    tempPath = toolPath + "/temp/"
    botMap = config["bottom_value"]
    for dm in config["abstract_domain"][3]:
        os.system("bash " + toolPath + "src/getFunDef.sh " + toolPath + "abstract_domain/" +
                  config["abstract_domain"][0] + " " + dm + " > " + tempPath + dm + "_gen")
        os.system("bash " + toolPath + "src/getFunDef.sh " + toolPath + "abstract_domain/" +
                  config["abstract_domain"][0] + " " + dm + " | sed 's/return.*/return " + botMap[dm] + ";/g' > "
                  + tempPath + dm)
        util.cleanBotFun(tempPath + dm)
        os.system("sed -i 's/{}/{}_c/g' ".format(dm,dm) + tempPath + dm)

'''
    this function will dump the transformers synthesised 

'''
def dumpCulpritTransformer(skfile, culpritFun, domainList, tempPath):
    for dls in domainList.keys():
        for culprit in domainList[dls]:
            # print(tempPath + culprit)
            util.emit_file(tempPath + culprit, skfile)
    

def getGammaCheck_c(config, domainMap):
    toolPath = config["basepath"]
    tempPath = toolPath + "/temp/"
    os.system("echo \"\" > contain")
    for i in domainMap.keys():
        os.system("bash " + toolPath + "src/"  +"getFunDef.sh " + toolPath + "abstract_domain/" + config["abstract_domain"][0] +
                  " GammaCheck" + i + " | sed 's/GammaCheck" + i + "/GammaCheck" + i +"_c/g' >> " + tempPath + "contain")

    absFun = config["abstract_domain"][3]

    for i in range(len(absFun)):
        os.system("sed -i 's/" + absFun[i] + "/" + absFun[i] + "_c/g' " + tempPath  + "contain")

    with open(tempPath + "contain") as f:
        con = f.readlines()
    return con

def dumpGammaCheck(culpritFun, domainMap, skfile, tail, tempDir):
    for i in culpritFun:
        util.emit_file(tempDir + i + "gamma" + tail, skfile)

def getAbsValTypeList(config, proto):
    concArgs = len(proto) - 1
    concreteFn = list(config["tosynthesize"])[0] 
    typeList = []

    # first add types of all abstract values
    for j in range(concArgs):
        for i in config["abstract_value"]:
            typeList.append(i[1][0])

    # lastly add the type of the counter-example
    typeList.append(proto[0]) # proto[0] is the return type of the function
    if concreteFn == "charAt":
        typeList[-2] = typeList[-1]
    return typeList

# this file just dump to file with proper format
# info contain [l, u, c]
# flag to decide to positive or negative example
# dumpCex(file1, label, info, 'n', maxsatFlag, proto)
def dumpCex(config, file1, label, info, flag, maxsatFlag, proto, gammaCheck, culprit):
    cex = ''
    notSign = ''
    countExpr = ''
    arrayFlag = 0

    if re.search("\[.*\]", proto[0]) and arrayFlag == 0:
        arrayFlag = 1

    concreteFn = list(config["tosynthesize"])[0]
    if "contains" in concreteFn:
        arrayFlag = 1

    if flag == 'n':
        notSign = '!'

        if (maxsatFlag == 1) and ("boot" not in label):
            cex += "\tif( %s == 0)\n" % label
            countExpr = "\t nCount += %s;\n" % label

    gammaArg = []
    typegammaArg = getAbsValTypeList(config, proto)
    typeCnt = 0
    for i in info:
        if arrayFlag == 0:  # type(i) != list:
            gammaArg.append(str(i))
        else:
            if type(i) == list:
                gammaArg.append("(" + typegammaArg[typeCnt] + ")" + str(i).replace('[', '{').replace(']', '}'))
            else:
                gammaArg.append(str(i))
        typeCnt += 1
    cons = []
    for dom in gammaCheck:
        if False:
            tcex = []
            for l in culprit:
                tcex.append(str(l) + '(' + ','.join(elem for elem in gammaArg[:-1]) + ')')
            tcex.append(gammaArg[-1])
            cons.append("GammaCheck" + dom + '(' + ','.join(elem for elem in tcex) +  ')')
        else:
            cons.append("GammaCheck" + dom + '(' + ','.join(elem for elem in gammaArg) + ')')

    if flag == 'p':
        cex += "\tassert (" + '&'.join(elem for elem in cons) + ");\n"

    if flag == 'n':
        cex += "\tassert (" + '||'.join('~(' + elem + ')' for elem in cons) + ");\n"

    
    cex += countExpr

    file1.writelines([cex])


# adds both positive and negative cex in the file pointed by file1
def addCex(config, file1, curNex, posex, maxsatFlag, proto, gammaCheck, culprit):
    for label, info in posex.items():
        dumpCex(config, file1, label, info, 'p', maxsatFlag, proto, gammaCheck, culprit)

    for label, info in curNex.items():
        dumpCex(config, file1, label, info, 'n', maxsatFlag, proto, gammaCheck, culprit)

