import json
import os
import sys

import lib.utility as util
from py_console import console

'''
    Collects i for all i \in DOMAINS , c' \notin \gamma(f_{Ei}^{#}(a_i))
    It returns all the domain names for which c' is not contained by the transformers

    parameters : config file
    returns    : list of domain names  
'''
def getCulpritDomainFuzz(fileName):
    with open(fileName) as f:
        names = f.readlines(fileName)
    names = [i.strip() for i in names]
    return names


'''
    function returns the set  of negative examples which are responsible for culrpit set
'''
def getCulpritNegExFuzz(config, negex, culprit, allDomains):
    toolPath = config["basepath"]
    file1 = open(toolPath + "temp/getCul.cc", "w")
    #file1.write("#include<stdio.h>\n")
    file1.write("#include <assert.h>\n")
    file1.write("#include <stdlib.h>\n")
    file1.write("#include <iostream>\n")
    file1.write("#include <inttypes.h>\n")
    if config["extlib"] != "":
        file1.write("#include \"" + toolPath  + "/external_lib/" + config["extlib"].replace(".so", ".h\"") + "\n")
    file1.write("#include <unistd.h>\n")
    file1.write("#include <fstream>\n")
    file1.write("#include <cstdio>\n")
    file1.write("#include \"vops.h\"\n")
    # file1.write("#include \"" + toolPath + "temp/f_synth_AFL.cpp\"\n")
    file1.write("using namespace std;\n")
    util.emit_file(toolPath + "abstract_domain/" + config["abstract_domain"][2], file1)
    util.emit_file(toolPath + "aux_function/" + config["aux_fun"][0], file1)
    # util.emit_file(toolPath + "/temp/f_synth_AFL.cpp", file1)
    # util.emit_file(toolPath + "/temp/f_synth_old.sk", file1)
    for i in config["abstract_domain"][3]:
        util.emit_file(toolPath + "temp/" + i + ".cpp", file1)
    file1.write("int main(){\n")
    file1.write("\tFILE *outfile = fopen(\"{}temp/negex.txt\", \"w\");\n".format(toolPath))
    
    '''
        we just have to check whether c' is in gammacheck or not for that transformer
    '''
    # it just maps domain name to its index in the config["domain"] list
    nameToIdx = {}
    for i in range(len(config["domains"])):
        nameToIdx[config["domains"][i][0]] = i

    # iterate over all the examples and dump the ids of the negative examples 
    # which violates the current transformer  
    functionProto = config["tosynthesize"][list(config["tosynthesize"].keys())[0]]
    # console.warn("Function prototype: ", functionProto)

    for nex in negex.keys():
        ex = negex[nex]
        # expecting ex = [[......],c'] where, [...] is the abstract value

        #example = ex[0][:len(config["abstract_value"]) * (len(functionProto) - 1)]
        example = ex[:len(config["abstract_value"]) * (len(functionProto) - 1)]

        exampleStr = ','.join([str(i) for i in example])

        gammaCheck = []
        culpritPrime = list(set(allDomains) - set(culprit))
        for k in culpritPrime:
            argsForCheck = []
            transList = config["domains"][nameToIdx[k]][1]
            for x in transList:
                argsForCheck.append(str(x) + '_c(' + exampleStr + ')')

            gammaCheck.append("GammaCheck" + k + "(" + ','.join([str(j) for j in argsForCheck]) + ', ' + str(ex[-1]) + ')')

        file1.write("\tif(!(" + ' && '.join([str(i) for i in gammaCheck]) + "))\n")
        file1.write("\t\tfprintf(outfile, \"" + nex + "\\n\");\n")

    file1.write("\tfclose(outfile);\n")
    file1.write("}\n")
    file1.close()
    os.system("g++ {}/temp/getCul.cc -I {}/include -L {}/external_lib -lmath -lm -g -w -o {}temp/getNex".format(toolPath, toolPath, toolPath, toolPath))
    print("g++ {}/temp/getCul.cc -I {}/include -L {}/external_lib -lmath -lm -g -w -o {}temp/getNex".format(toolPath, toolPath, toolPath, toolPath))
    os.system("{}/temp/getNex".format(toolPath))
    with open(toolPath + "temp/negex.txt") as f:
        culNegEx = f.readlines()

    # culNegEx is the set of the small negative example responsible for the culprit domains
    culNegEx = [str(i).strip() for i in culNegEx]
    culNegExPrime = list(set(negex.keys()) - set(culNegEx))
    culNegExMap = {} # map from label to values
    for i in culNegExPrime:
        culNegExMap[i] = negex[i]

    console.error("negex, culNegEx, culNegExPrime,  culNegExMap: ", negex, culNegEx, culNegExPrime,  culNegExMap)
    # exit()
    return culNegExMap

if __name__=="__main__":
    with open(sys.argv[1]) as jsonFile:
        config = json.load(jsonFile)
    getCulpritNegExFuzz(config, {"test1": [[1,2,3,4,5,6,7,8,3,9,0],33], "test2": [[1,2,1,4,5,6,7,8,3,9,0],223]}, ["oddIntv", "evenIntv"])
