#!/usr/bin/python3

import json
import os
import re
import sys
from copy import copy
from functools import reduce
import time 
from py_console import console

sys.path.insert(0, 'lib/')
import lib.utility as util
import lib.oracles as oracles
import lib.sketchUtil as skutil
import lib.soundnessCheck as soundnessCheck

# positve contains positive examples
# negative contains negative examples
cexMap = {"Positive": {}, "Negative": {}}


# get the template for sketch
def getInitializeTemplate(config):
    toolPath = config["basepath"]
    tempPath = toolPath + "/temp/"

    with open(toolPath + "dsl/" + config["dsl"], "r") as file1:
        dsl = file1.readlines()

    with open(toolPath + "aux_function/" + config["aux_fun"][1], "r") as file1:
        aux = file1.readlines()


    return dsl, aux


def readJSON(fileName):
    with open(sys.argv[1]) as jsonFile:
        return json.load(jsonFile)


# initialise all the files present in the list ls
def initializeTempFiles(tempPath, ls):
    for i in ls:
        with open(tempPath + i, "w") as file1:
            file1.write("")

'''
termination condition checks whether isSP flag for each domain is True
'''
def terminationCondition(isSP):
    flag = bool(reduce(lambda x, y: x and y,  list(isSP.values())))
    return not flag

def amurth(fileName):
    start = time.time()
    isPrecise = {}
    isSound = {}

    soundnessCount = {}
    precisionCount = {}

    # reading the json file
    config = readJSON(fileName)

    funcName = list(config["tosynthesize"].keys())[0]

    # checking whether array is in the concrete function or not
    arrayFlag = 0
    if re.search("\[.*\]", config["abstract_value"][0][1][0]):
        arrayFlag = 1

    toolPath = config["basepath"]
    tempPath = toolPath + "/temp/"

    domainMap = {}
    isSP = {}

    # initialise map for each domain for negative examples
    for info in config["domains"]:
        domainMap[info[0]] = info[1]
        cexMap["Negative"][info[0]] = {}
        cexMap["Positive"][info[0]] = {}
        isPrecise[info[0]] = False
        isSound[info[0]]   = False
        soundnessCount[info[0]] = 0
        precisionCount[info[0]] = 0
        isSP[info[0]] = False
    # initialise the C files
    util.createHeaderDomain(config)

    generator, aux_func = getInitializeTemplate(config)

    domainPy = util.getPythonHandle(tempPath, toolPath + "abstract_domain/" + config["abstract_domain"][1])
    pos, neg = domainPy.getBootstrap(5)

    bootCnt = 0
    for dom, listEx in pos.items():
        for i in listEx:
            label = "boot%s" % bootCnt
            cexMap["Positive"][dom][label] = i
            bootCnt += 1

    # print("neg items", neg.items())
    for dom, listEx in neg.items():
        for i in listEx:
            label = "boot%s" % bootCnt
            cexMap["Negative"][dom][label] = i
            bootCnt += 1

    culpritSet = []
    for i in domainMap.keys():
        culpritSet.append(i)

    cexCnt = bootCnt

    nonDet = True

    skutil.createGenFiles(config)

    logFile = "log_" + funcName + ".txt"
    initializeTempFiles(tempPath, [logFile, "sketchSoundness.sk"])
    mainLoop = 1
    while terminationCondition(isSP): #(not isSound) or (not isPrecise):
        console.success("Counting main loop: " + str(mainLoop))
        mainLoop += mainLoop + 1
        for currentDom in domainMap.keys():
            console.success("Starting with: " + currentDom)
            while (not isSound[currentDom]) or (not isPrecise[currentDom]):
                console.success(currentDom + ": sound: " + str(isSound[currentDom]) + 
                                ", precise: " + str(isPrecise[currentDom]))
                if nonDet:
                    nonDet = False
                    domainMapNew = {}
                    domainMapNew[currentDom] = copy(domainMap[currentDom])
                    res = oracles.checkSoundness(config, domainMapNew, logFile, cexMap)
                    if res == "UNSAT":
                        console.success("UNSAT in soundness check, so closing the shop for " + currentDom)
                        with open(logFile, "a") as f:
                            f.write("UNSAT in soundness check for: " + currentDom + "\n")

                        isSound[currentDom] = True
                    else:
                        posEx = soundnessCheck.processPosEx(config, arrayFlag)
                        if posEx in cexMap["Positive"].values():
                            console.error("Same example generated. So depressing!!")
                            console.success(
                                ("Generated positive example: " + str(posEx).replace("[", "").replace("]", "")))
                            exit()

                        totalPosEx = 0
                        for keys, values in cexMap["Positive"].items():
                            totalPosEx = totalPosEx + len(values)

                        labelName = "posex" + str(totalPosEx)
                        cexCnt += 1

                        for dn in domainMap.keys():
                            cexMap["Positive"][dn][labelName] = posEx

                        with open(logFile, "a") as f:
                            f.writelines("Generated positive example: " + str(posEx).replace("[", "").replace("]", "") + "\n")
                        console.success(("Generated positive example: " + str(posEx).replace("[", "").replace("]", "")))
                        isPrecise[currentDom] = False
                        isSound[currentDom] = False
                    precisionCount[currentDom] = 1
                    soundnessCount[currentDom] += 1

                else:

                    initializeTempFiles(tempPath, ["syn_func", "syn_func.cpp", "f_synth_old.sk", "f_synth_AFL.cpp"])
                    domainMapNew = {}
                    domainMapNew[currentDom] = copy(domainMap[currentDom])
                    res, cexCnt = oracles.checkPrecision(config, "dump", logFile, soundnessCount[currentDom], precisionCount[currentDom],
                                                    domainMapNew, generator, aux_func, cexMap, domainPy, cexCnt)

                    precisionCount[currentDom] += 1
                    if "UNSAT" in res:
                        console.error("UNSAT in precision check for: " + currentDom)

                        nonDet = True
                        isPrecise[currentDom] = True

                        # code for maxsynth
                        initializeTempFiles(tempPath, ["syn_func", "syn_func.cpp", "f_synth_old.sk", "f_synth_AFL.cpp"])

                        culpritSet = []
                        for i in domainMapNew.keys():
                            culpritSet.append(i)

                        for dname in domainMapNew.keys():
                            delta = oracles.maxSatSynthesize(config, "dump", logFile, soundnessCount[currentDom],
                                                             precisionCount[currentDom],
                                                             generator, aux_func, dname, cexMap["Negative"][dname],
                                                             cexMap, domainMapNew, domainPy, cexCnt)

                            console.warn("Dropped by MAXSAT for " + dname + ": " + str(delta))
                            nex = delta

                            for i in domainMap[dname]:
                                os.system(
                                    "bash " + toolPath + "src/getFunDef.sh " + tempPath + "result_file " + str(i) +
                                    " | sed 's/" + str(i) + "/" + str(i) + "_c/g' >> " + tempPath + "syn_func")

                                # for cpp version of sketch
                                os.system(
                                    "bash " + toolPath + "src/getFunDef.sh " + tempPath + "result_file_cpp " + str(i) +
                                    " | sed 's/" + str(i) + "/" + str(i) + "_c/g' >> " + tempPath + "syn_func.cpp")

                        toSyn = []
                        for dname in culpritSet:
                            for i in domainMap[dname]:
                                toSyn.append(i)

                        util.removeRef(config)

                        for i in config["abstract_domain"][3]:
                            os.system("bash " + toolPath + "src/getFunDef.sh " + tempPath + "f_synth_old.sk " +
                                str(i) + "_c > " + tempPath + "checkTrans")

                            if os.stat(tempPath + "checkTrans").st_size > 5:
                                os.system("cat " + tempPath + "checkTrans > " + tempPath + i)
                                os.system(
                                    "bash " + toolPath + "src/getFunDef.sh " + tempPath + "f_synth_AFL.cpp " + str(i) +
                                    "_c > " + tempPath + i + ".cpp")

                            elif i in toSyn:
                                console.error("Oh My GOD: {}".format(i))
                                exit()

                    else:
                        isSound[currentDom]   = False
                        isPrecise[currentDom] = False
                        for i in domainMap.keys():
                            if i == currentDom:
                                continue
                            isPrecise[i] = False
                            isSound[i]   = False
                            isSP[i]      = False

            isSP[currentDom] = True  # assuming current domain is sound and precise

    console.success("Exiting as both soundness and precision check became True")
    end = time.time()
    with open(logFile, "a") as logF:
        logF.write("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        logF.write("Synthesized transformers are as follows:\n")
        logF.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        for dom, absList  in domainMap.items():
            logF.write("For domain: " + dom + "\n")
            logF.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
            for i in absList:
                logF.write("For " + i + ":\n")
                logF.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                util.emit_file(tempPath + i, logF)
                logF.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        logF.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        logF.write("\nTotal time (s): " + str(end-start))


if __name__ == "__main__":
    amurth(sys.argv[1])
