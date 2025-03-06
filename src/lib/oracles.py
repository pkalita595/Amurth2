"""
    This file consist of the two oracles and its dependencies
"""

import os
import time

import lib.culprit as cul
import lib.sketchUtil as sk
import lib.utility as util
import lib.soundnessCheck as soundnessCheck

from py_console import console
from goto import with_goto



def maxSatSynthesize(config, sketchFile, reportFile, outerLoop, counter, generator, aux_func, dname, negexSubset,
                     cexMap, domainMap, domainPy, cexCnt):
    console.info("MaxSatSynthesize is being called")
    toolPath = config["basepath"]
    tempPath = toolPath + "/temp/"

    console.info("In MaxSatSynthesize with culprit domain: " + str(dname))
    sketchF = tempPath + "sketch/%s_%s_%s_%s_MAXSAT.sk" % (sketchFile, outerLoop, counter, dname)

    # resetting the file
    with open(sketchF, "w") as file1:
        file1.write("")
    skfile = open(sketchF, "a")
    sk.dumpSketchFile(config, skfile, generator, aux_func, dname, domainMap, negexSubset, cexMap["Positive"][dname], 0, 1)
    skfile.close()

    start = time.time()
    os.system("bash " + toolPath + "src/sketch_run.sh " + sketchF + " " + toolPath)
    end = time.time()
    console.error("Time spent in sketch (maxSatSynthesize): " + str(end - start))

    # now check the result from sketch_result
    with open(tempPath + "sketch_result", "r") as file1:
        res = file1.readlines()
    console.info("MaxSatSynthesize result for " + sketchF + ": " + str(res[0]).strip())

    if res[0].strip() == "SAT":
        # need to collect the negative example and add it to the cexMap
        holeFile = config["basepath"] + "/temp/hole.xml"
        delta, boolFlag, cexCnt = sk.processHoles(config, sketchF, holeFile, 1, reportFile, cexMap, negexSubset, 
                                                  dname, domainMap, domainPy, cexCnt)
        return delta
    else:
        console.error("Maxsat got unsat", sketchF)
        exit()


def consistentCheck(config, sketchFile, reportFile, outerLoop, counter, generator, aux_func, dname,
                     cexMap, domainMap, domainPy, cexCnt):
    console.info("consistentCheck is being called")
    posexSubset = cexMap["Positive"][dname]
    negexSubset = cexMap["Negative"][dname]

    if len(posexSubset) == 0 and len(negexSubset) == 0:
        console.error("Both sets of examples are empty")
        exit()

    toolPath = config["basepath"]
    tempPath = toolPath + "/temp/"

    console.info("In consistency check with culprit domain: " + str(dname))
    sketchF = tempPath + "sketch/%s_%s_%s_%s_Consistent.sk" % (sketchFile, outerLoop, counter, dname)

    # resetting the file
    with open(sketchF, "w") as file1:
        file1.write("")
    skfile = open(sketchF, "a")
    sk.dumpSketchFile(config, skfile, generator, aux_func, dname, domainMap, negexSubset, posexSubset, 0, 1)
    skfile.close()

    start = time.time()
    os.system("bash " + toolPath + "src/sketch_run.sh " + sketchF + " " + toolPath)
    end = time.time()
    console.error("Time spent in sketch (CheckConsistency): " + str(end - start))

    # now check the result from sketch_result
    with open(tempPath + "sketch_result", "r") as file1:
        res = file1.readlines()
    console.info("CheckConsistency result for " + sketchF + ": " + str(res[0]).strip())

    if res[0].strip() == "SAT":
        # need to collect the negative example and add it to the cexMap
        holeFile = config["basepath"] + "/temp/hole.xml"
        delta, boolFlag, cexCnt = sk.processHoles(config, sketchF, holeFile, 1, reportFile, cexMap, negexSubset, 
                                          dname, domainMap, domainPy, cexCnt)
        return delta, cexCnt
    else:
        console.error("Maxsat got unsat", sketchF)
        exit()

# lets modify cexMap as cexMap = {"Positive": {}, "Negative":{"dname":{}}}
# returns result, culprit_domain_name, negative_examples_for_that_domain, current_-ve_example
def checkPrecision(config, sketchFile, reportFile, outerLoop, counter, domainMap, generator, aux_func, cexMap, domainPy, cexCnt):
    console.info("CheckPrecision is being called")

    toolPath = config["basepath"]
    tempPath = toolPath + "/temp/"

    negex = cexMap["Negative"]  # trying to create a list of negative example
    newPrecCex = {} # map for new negative examples for each domain
    unsatCounter = 0

    with open(reportFile, "a") as f:
        f.writelines("~~~~~ sound/precise: " + str(outerLoop) + "/" + str(counter) + " ~~~~~\n")
    for dname, culprit in domainMap.items():
        assert isinstance(culprit, list)
        if False: #len(negex) > 0:
            curNex = cul.getCulpritNegExFuzz(config, negex, [dname], domainMap.keys())
        else:
            curNex = negex[dname]

        console.info("In check precision loop with culprit domain: " + str(culprit))
        sketchF = tempPath + "sketch/%s_%s_%s_%s.sk" % (sketchFile, outerLoop, counter, dname)

        # resetting the file
        with open(sketchF, "w") as file1:
            file1.write("")
        skfile = open(sketchF, "a")
        # function to create sketch file
        sk.dumpSketchFile(config, skfile, generator, aux_func, dname, domainMap, curNex, cexMap["Positive"][dname], 1, 1)
        skfile.close()

        # call sketch_run.sh
        print(sketchF)
        start = time.time()
        os.system("bash  " + toolPath + "src/sketch_run.sh " + sketchF + " " + toolPath)
        end = time.time()
        console.error("Time spent in sketch (CheckPrecision): " + str(end - start))
        # sketchCount += 1

        # now check the result from sketch_result
        with open(tempPath + "sketch_result", "r") as file1:
            res = file1.readlines()
        console.info("Precision check result for " + sketchF + ": " + str(res[0]).strip())

        if res[0].strip() == "SAT":
            # need to collect the negative example and add it to the cexMap
            holeFile = config["basepath"] + "/temp/hole.xml"
            newCex, exampleRes, cexCnt = sk.processHoles(config, sketchF, holeFile, 0, reportFile, cexMap, curNex, 
                                                         dname, domainMap, domainPy, cexCnt)

            newPrecCex[dname] = newCex

            with open(reportFile, "a") as f:
                f.writelines("~~~~~ " + dname + " ~~~~~\n")
                f.writelines("Counter example: {}\n".format(newCex))
                f.writelines("~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


            if exampleRes != False:
                with open(reportFile, "a") as f:
                    f.writelines("\n~~~~~ Example is positive so discarding synthesis call ~~~~~\n")
                    f.writelines("Cex: " + str(newCex) + "\n")
                console.info("\n~~~~~ Example is positive so discarding synthesis call ~~~~~\n")
                console.info("Cex: ", newCex)
                continue

            # dumping the new functions generated
            for i in domainMap[dname]:
                os.system("bash " + toolPath + "src/getFunDef.sh " + tempPath + "result_file " + str(i) +
                          " | sed 's/" + str(i) + "/" + str(i) + "_c/g' >> " + tempPath + "syn_func")
                # for cpp version of sketch
                os.system("bash " + toolPath + "src/getFunDef.sh " + tempPath + "result_file_cpp " + str(i) +
                          " | sed 's/" + str(i) + "/" + str(i) + "_c/g' >> " + tempPath + "syn_func.cpp")

                util.removeRef(config)  # remove the ref

                os.system(
                    "bash " + toolPath + "src/getFunDef.sh " + tempPath + "f_synth_old.sk " + str(i) + "_c > " +
                    tempPath + "checkTrans")

                with open(reportFile, "a") as f:
                    lines = []
                    with open("checkTrans", "r") as fF:
                        lines = fF.readlines()
                    f.writelines(lines)
                    f.writelines("\n~~~~~~~~~~\n")

                if os.stat(tempPath + "checkTrans").st_size > 5:
                    os.system("cat " + tempPath + "checkTrans > " + tempPath + i + ".temp")
                    os.system("bash " + toolPath + "src/getFunDef.sh " + tempPath + "f_synth_AFL.cpp " + str(i) +
                              "_c > " + tempPath + i + ".cpp.temp")
                else:
                    console.error("Empty definition in check precision for -> {}".format(i))
                    exit()

            with open(reportFile, "a") as f:
                f.writelines("~~~~~~~~~~~~\n")

        else:
            unsatCounter += 1
            if unsatCounter == len(domainMap.keys()):
                return "UNSAT", cexCnt #, dname, {}, {}


    # assuming checkPrecision for all the domains succeeded
    if exampleRes == False:
        for dname, culprit in domainMap.items():
            for i in culprit:
                os.system("cat " + tempPath + i + ".temp  > " + tempPath + i )
                os.system("cat " + tempPath + i + ".cpp.temp" + " > " + tempPath + i + ".cpp")

    return "SAT", cexCnt # , dname, curNex, newCex

'''
    check soundness oracle is being implemented here. 
    It finds the culprit domains who breaks the gamma check and try to synthesize 
    culprit transformers using maxsat solver
'''


def checkSoundness(config, domainMap, logFile, cexMap):
    soundnessCheck.generateSketchSoundnessFile(config, domainMap)
    res = soundnessCheck.runSoundnessCheck(config)
    return res
