import os
import re

from py_console import console
import xml.etree.ElementTree as ET

import lib.utility as util
import lib.sketchUtil as skutil

def dumpSynthesizedTransformers(tempPath, domainMap, outputFile):
    for dname, culprit in domainMap.items():
        for i in culprit:
            util.emit_file(tempPath+i, outputFile)

def dumpSketchForSoundnessArray(config, domainMap, proto, inputLen, concreteFn, dumpFile):
    for j in range(1, inputLen + 1):
        i = str(j)
        if proto[j] == "int":
            util.emit(["\tint arg" + i + " = ??;\n"], dumpFile)
        else:
            util.emit(["\t" + proto[j] + " arg" + i + " = ??;\n"], dumpFile)
            util.emit(["\tassert arg" + i + " != {0,0,0,0,0};\n"], dumpFile)
            util.emit(["\tcreateString(arg" + i + ", ??);\n"], dumpFile)

        absValue = config["abstract_value"]

        stringDom = config["string_domain"]
        if len(set(proto[1:])) == 1:
            if skutil.isInputArray(proto[j]):
                if stringDom == "safe" or stringDom == "jsai":
                    util.emit(["\t" + config["abstract_value"][0][1][0] + " " + config["abstract_value"][0][0] +
                               str(j) + " = ??;\n"], dumpFile)
                    util.emit(["\t" + config["abstract_value"][1][1][0] + " " + config["abstract_value"][1][0] +
                               str(j) + " = ??;\n"], dumpFile)
        else: # for charAt: different type of arguments
            if stringDom == "safe" or stringDom == "jsai":
                if skutil.isInputArray(proto[j]):
                    util.emit(["\t" + config["abstract_value"][0][1][0] + " " + config["abstract_value"][0][0] +
                               str(j) + " = ??;\n"], dumpFile)
                    util.emit(["\t" + config["abstract_value"][1][1][0] + " " + config["abstract_value"][1][0] +
                               str(j) + " = ??;\n"], dumpFile)
                elif proto[j] == "int":
                    if concreteFn == "charAt":
                        util.emit(["\tintCP intVal = new intCP();\n"], dumpFile)
                        util.emit(["\tintVal.isTop = 0;\n"], dumpFile)
                        util.emit(["\tintVal.isBot = 0;\n"], dumpFile)
                        util.emit(["\tintVal.value = arg2;\n"], dumpFile)
                        util.emit(["\tassert arg2 < getLength((int[2*N])arg1);\n"], dumpFile)
            
            
    domainMapNew = {}
    for info in config["domains"]:
        domainMapNew[info[0]] = info[1]

    # dump the gammaCheck
    absValue = config["abstract_value"]
    for i in range(1, inputLen + 1):
        if proto[i] == "int":
            continue
        args = []
        for j in range(len(absValue)):
            args.append(absValue[j][0] + str(i))
        args.append("arg" + str(i))
        argStr = ','.join(args)
        dumpFile.writelines("\tassert gammaCheck( " + argStr + ");\n")

    absValList = config["abstract_domain"][3]

    domArgs = []
    for i in range(1, inputLen + 1):
        for j in absValue:
            domArgs.append(j[0] + str(i))
    
    if concreteFn == "charAt":
        if stringDom == "safe":
            domArgs = ["ssk_val1", "no_val1", "intVal"]
        elif stringDom == "jsai":
            domArgs = ["ssk_val1", "nos_val1", "intVal"]
            

    args = {}
    print("domainMap: ", domainMap)
    output = {}
    for dname, blah in domainMap.items():
        args[dname] = []
        for i in blah:
            util.emit(["\t" + config["return_type"][i] + " " + dname + i + " = " + i + "_c(" + ','.join(domArgs) + ");\n"], dumpFile)
            args[dname].append(dname + i)
        output[dname] = concreteFn + "(" + ', '.join(["arg" + str(k) for k in range(1, inputLen + 1)]) + ")"
        args[dname].append("output")



    checkArgs = []
    for dname, blah in domainMap.items():
        util.emit(["\t" + proto[0] + " output = " + output[dname] + ";\n"], dumpFile)
        util.emit(["\tassert output == ??;\n"], dumpFile)
        # in case of contains we want boolean gammaCheck
        if "contains" in concreteFn:
            checkArgs.append("~(gammaCheckSoundBool" + dname + "(" + ', '.join(args[dname]) + "))")
        else:
            checkArgs.append("~(gammaCheckSound" + dname + "(" + ', '.join(args[dname]) + "))")

    util.emit(["\tassert " + "||".join(checkArgs) + ";\n"], dumpFile)


def generateSketchSoundnessFile(config, domainMap):
    print("Domain map in soundness check: " + str(domainMap))
    toolPath = config["basepath"]
    file1 = open(toolPath + "temp/sketchSoundness.sk", "w")
    concreteFn = list(config["tosynthesize"])[0]
    proto = config["tosynthesize"][concreteFn]
    inputLen = len(proto) - 1
    absValue = config["abstract_value"]
    arrayFlag = 0
    domLogicSpec = ""

    if "soundness_sem" not in config.keys():
        domDir = config["abstract_domain"][0]
        domDir = domDir.split('/')[0]
        with open(toolPath + "abstract_domain/" + domDir + "/soundnessCheckDep.sk") as f:
            domLogicSpec = f.readlines()
    else:
        filename = toolPath + "abstract_domain/" + config["soundness_sem"]
        with open(filename) as f:
            domLogicSpec = f.readlines()

    file1.writelines(domLogicSpec)


    dumpSynthesizedTransformers(toolPath + "temp/", domainMap, file1)

    if concreteFn == "add" or concreteFn == "sub" or concreteFn == "abs" or concreteFn == "increment":
        with open(toolPath + "external_lib/logicalSpecInterval.sk") as f:
            logicalSpec = f.readlines()
    else:
        with open(toolPath + "external_lib/logicalSpec.sk") as f:
            logicalSpec = f.readlines()


    # load all concrete function
    file1.writelines(logicalSpec)


    file1.writelines("\n")

    util.emit_file(toolPath + "aux_function/" + config["aux_fun"][1], file1)

    # include all synthesized transformers
    file1.writelines("\nharness void main(){\n")

    

    if re.search("\[.*\]", proto[0]) and arrayFlag == 0:
        arrayFlag = 1

    if "contains" in concreteFn:
        arrayFlag = 1

    if arrayFlag == 0: # not string
        inputArgs = [] # might use these for some reason I guess
        # dump the holes
        for j in range(1, inputLen + 1):
            i = str(j)
            util.emit(["\tint arg" + i + "sign = ??;\n"], file1)
            util.emit(["\tint arg" + i + "val = ??;\n"], file1)
            util.emit(["\tint arg" + i + " = (arg" + i + "sign == 0) ? arg" + i + "val : -arg" + i + "val;\n"], file1)
            inputArgs.append("arg"+i)

        # for dname, culprit in domainMap.items():

        for j in range(1, inputLen + 1):
            for i in range(len(absValue)):
                util.emit(["\tint " + absValue[i][0] + str(j) + "sign" + "= ??;\n"], file1)
                util.emit(["\tint " + absValue[i][0] + str(j) + "val" + "= ??;\n"], file1)

        for j in range(1, inputLen + 1):
            for i in range(len(absValue)):
                util.emit(["\tint " + absValue[i][0] + str(j) + " = (" + absValue[i][0] + str(j) + "sign" + " == 0 ? " +
                      absValue[i][0] + str(j) + "val" + " : -" + absValue[i][0] + str(j) + "val" + ");\n"], file1)

        for i in range(1, inputLen + 1):
            util.emit(["\tassert (leftOdd{} <= leftEven{} && leftEven{} <= rightOdd{}) || "
                       "(leftEven{} <= leftOdd{} && leftOdd{} <= rightEven{});\n".format(i, i, i, i, i, i, i, i)],
                      file1)

        domainMapNew = {}
        for info in config["domains"]:
            domainMapNew[info[0]] = info[1]

        # dump the gammaCheck
        cnt = 0
        for dname, absList in domainMapNew.items():
            for i in range(1, inputLen + 1):
                args = []
                for j in absList:
                    args.append(
                        j.replace("abs", "") + str(
                            i))  # todo: its a hack to convert transformer name to value name: Fix it

                args.append("arg" + str(i))
                argStr = ','.join(args)

                file1.writelines("\tassert gammaCheckSound" + dname + "(" + argStr + ");\n")

        domArgs = []
        for i in range(1, inputLen + 1):
            for j in absValue:
                domArgs.append(j[0] + str(i))

        args = {}
        for dname, blah in domainMap.items():
            args[dname] = []
            for i in blah:
                util.emit(["\tint " + dname + i + " = " + i + "_c(" + ','.join(domArgs) + ");\n"], file1)
                args[dname].append(dname + i)
            args[dname].append(concreteFn + "(" + ', '.join(["arg" + str(k) for k in range(1, inputLen + 1)]) + ")")

        checkArgs = []
        for dname, blah in domainMap.items():
            checkArgs.append("~(gammaCheckSound" + dname + "(" + ', '.join(args[dname]) + "))")

        util.emit(["\tassert " + "||".join(checkArgs) + ";\n"], file1)


    else:
        dumpSketchForSoundnessArray(config, domainMap, proto, inputLen, concreteFn, file1)


    util.emit(["}\n"], file1)


def processPosEx(config, arrayFlag):
    if arrayFlag == 0:
        return processPosExIntv(config)
    else:
        return processPosExString(config)

def processPosExString(config):
    tempPath = config["basepath"] + "/temp/"
    concreteFn = list(config["tosynthesize"])[0]
    proto = config["tosynthesize"][concreteFn]
    inputLen = len(proto) - 1
    absValue = config["abstract_value"]
    tree = ET.parse(tempPath + "sound.xml")
    root = tree.getroot()
    holeMap = skutil.getHoleMapArray(root)
    posex = []
    sketchFile = tempPath + "sketchSoundness.sk"
    for j in range(1, inputLen + 1):
        if proto[j] == "int":
            valLine = skutil.getLineNo(sketchFile, "int arg2")
            posex.append(f"new intCP(isTop = 0, isBot = 0, value = {holeMap[valLine]} )")
            continue
        for i in range(len(absValue)):
            try:
                valLine = skutil.getLineNo(sketchFile, absValue[i][1][0] + " " + absValue[i][0] + str(j))
                if valLine == -1:
                    console.error("Got -1 from getLineNo for " + absValue[i][0] + str(j))
                else:
                    posex.append(holeMap[valLine])
            except:
                print("key error in " + absValue[i][0] + str(j))

    outputLine = skutil.getLineNo(sketchFile, "assert output")
    if outputLine == -1:
        raise FileNotFoundError
    posex.append(holeMap[outputLine])
    console.info("posex found: ", posex)
    if config["string_domain"] == "safe":
        with open(tempPath + "posex.txt", "w") as f:
            for i in posex:
                f.writelines(str(i).replace('[', '').replace(']', '') + "\n")

    return posex


def processPosExIntv(config):
    tempPath = config["basepath"] + "/temp/"
    concreteFn = list(config["tosynthesize"])[0]
    proto = config["tosynthesize"][concreteFn]
    inputLen = len(proto) - 1
    absValue = config["abstract_value"]
    tree = ET.parse(tempPath + "sound.xml")
    root = tree.getroot()
    holeMap = skutil.getHoleMap(root)

    posex = []
    sketchFile = tempPath + "sketchSoundness.sk"
    for j in range(1, inputLen + 1):
        for i in range(len(absValue)):
            try:
                signLine = skutil.getLineNo(sketchFile, "int " + absValue[i][0] + str(j) + "sign" )
                if signLine == -1:
                    console.error("Got -1 from getLineNo for " + absValue[i][0] + str(j) + "sign")
            except:
                print("key error in " + absValue[i][0] + str(j) + "sign")

            try:
                valLine = skutil.getLineNo(sketchFile, "int " + absValue[i][0] + str(j) + "val")
                if valLine == -1:
                    console.error("Got -1 from getLineNo for " + absValue[i][0] + str(j) + "val")
            except:
                print("key error in " + absValue[i][0] + str(j) + "val")
            signval = int(holeMap[signLine])
            value   = int(holeMap[valLine])
            posex.append(value if signval == 0 else -value)

    argList = []
    for j in range(1, inputLen + 1):
        signLine = skutil.getLineNo(sketchFile, "int arg" + str(j) + "sign")
        valLine  = skutil.getLineNo(sketchFile, "int arg" + str(j) + "val")
        signval  = int(holeMap[signLine])
        value    = int(holeMap[valLine])
        argList.append(value if signval == 0 else -value)

    fPrime = callConcreteFn(argList, config)
    posex.append(fPrime)
    return posex

'''
function to call the concrete spec: IDK best way to do that
for now lets settle with the python interfaces
'''
def callConcreteFn(argList, config):
    toolPath = config["basepath"]
    tempPath = toolPath + "/temp/"
    print(toolPath + "abstract_domain/" + config["abstract_domain"][1])
    domainPy = util.getPythonHandle(tempPath, toolPath + "abstract_domain/" + config["abstract_domain"][1])
    fPrime = domainPy.concreteFn(*argList) # add main function inside concreteFn
    return fPrime


def runSoundnessCheck(config):
    '''
    It just run the sketch file and returns whether sketch gives UNSAT or SAT
    :return: SAT or UNSAT
    '''
    tempPath = config["basepath"] + "/temp/"
    os.system("rm {}/sketchSoundness.cpp sound.xml".format(tempPath))
    os.system("sketch --fe-output-xml {}/sound.xml {}/sketchSoundness.sk --fe-output-test --slv-timeout 20 > /dev/null 2>&1"
              .format(tempPath, tempPath))

    if os.path.exists(tempPath + "sketchSoundness.cpp"): # SAT CASE
        return "SAT"
    else:
        return "UNSAT"
