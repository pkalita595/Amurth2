import functools
import os
import re

from py_console import console


'''
takes a file name containing single function,
removes all statement inside the function except return statement
'''
def cleanBotFun(filename):
    defFlag = 0
    with open(filename) as f:
        dump = f.readlines()
    newDump = []
    for line in dump:
        if '{' in line and defFlag == 0:
            defFlag = 1
            newDump.append(line)
        if defFlag:
            if "return" in line:
                newDump.append(line)
                defFlag = 0
        else:
            newDump.append(line)

    with open(filename, 'w') as f:
        f.writelines(newDump)


# returns the handle for domainPy
# which contains the bootstrap examples
'''
    #solution by chatGPT
    import imp

    # Path to the module
    module_path = "./temp/domainPy.py"
    module_name = "domainPy"

    # Load the module
    module = imp.load_source(module_name, module_path)

    # Now you can use the module
    print(module.some_function())
'''

def getPythonHandle(temp, pyfile):
    try:
        os.system("cp {} {}/domainPy.py".format(pyfile, temp))
        print("cp {} {}/domainPy.py".format(pyfile, temp))
        moduleName = (temp + "/domainPy").replace('//','.').replace('/','.')[1:]
        handle = __import__("domainPy", globals(), locals(), [], 0)
        return handle
    except:
        console.error("Couldnot import domainPy.py properly :(")
        exit()


#it create the header file for abstract domain c functions
def createHeaderDomain(config):
    toolPath = config["basepath"]
    tempPath = toolPath + "/temp/"
    tosynthesizeProto = list(config["tosynthesize"].values())[0]

    f1 = open(tempPath + "domain.h", 'w')
    absArg = ""
    for i in config["abstract_value"]:
        absArg += i[1][0] + ", "
    #f1.write("#include \"" + toolPath + "aux_function/" + config["aux_fun"][0] +"\"")
    f1.write("extern \"C\" int Gamma(" + absArg + tosynthesizeProto[0] + ");\n")
    f1.write("extern \"C\" " + config["abstract_value"][0][1][0] + "* Beta(" + tosynthesizeProto[0] + ");\n")
    f1.write("extern \"C\" " + config["abstract_value"][0][1][0] + "* GammaCheck(" + absArg[:-2] + ");\n")
    f1.write("extern \"C\" " + config["abstract_value"][0][1][0] + "* Join(" + absArg + absArg[:-2] + ");\n")
    f1.close()
    #
    os.system("cp " + toolPath + "abstract_domain/" + config["abstract_domain"][2] + " "+ tempPath  +"domain.cc")
    os.system("g++ -fPIC -shared -o "+  tempPath +"domain.so " + tempPath + "domain.cc" + " " + toolPath + "aux_function/" + config["aux_fun"][0])

'''
dumping to file
s:    file name not the file handle
fPtr: file handle not the name
'''
def emit_file(s, fPtr):
    with open(s) as langfile:
        fPtr.write(langfile.read() + '\n')

#function to create string from given list
def emit(s, fPtr):
    t = functools.reduce(lambda a, b: str(a) + " " + str(b), s)
    fPtr.write(t)


def comment_replacer(match):
    start, mid, end = match.group(1, 2, 3)
    if mid is None:
        # single line comment
        return ''
    elif start is not None or end is not None:
        # multi line comment at start or end of a line
        return ''
    elif '\n' in mid:
        # multi line comment with line break
        return '\n'
    else:
        # multi line comment without line break
        return ' '


def remove_comments(text):
    # following code is taken from
    # https://stackoverflow.com/questions/844681/python-regex-question-stripping-multi-line-comments-but-maintaining-a-line-brea

    comment_re = re.compile(
        r'(^)?[^\S\n]*/(?:\*(.*?)\*/[^\S\n]*|/[^\n]*)($)?',
        re.DOTALL | re.MULTILINE
    )

    return comment_re.sub(comment_replacer, text)


# end of copied code


auxFunName = ["min", "max", "concat", "getLength", "unionSet", "intersectionSet", "contains", "isSubset",
              "CharSetUnion", "CharSetIntersection", "sizeSet", "isElemPresent", "trim", "intToBit", "reverseBV",
              "rotateLeft", "rotateRight", "isEqual", "isEqualBV", "bitToInt", "interval", "modular", "cardinality",
              "bvlshift", "bvrshift", "arithRShift", "wrappedIn", "getVal", "wrappedtrunc", "wrapped", "bvNot",
              "overflow", "isEven", "isOdd", "getNOFromSSK", "getNOSFromSSK", "toLower", "toUpper", "intTrim", "toLowerSet",
              "toUpperSet", "trimSet", "containsSet", "charAtSet"]


# function to remove the last return argument of the function and chnageviod to the return type.
def removeRefCPP(config):
    tempPath = config["basepath"] + "/temp/"
    file1 = open(tempPath + "syn_func.cpp", 'r')
    file2 = open(tempPath + "f_synth_AFL.cpp", "a")
    tosynthesize = list(config["tosynthesize"].keys())[0]
    tosynthesizeProto = config["tosynthesize"][tosynthesize]
    arrayFlag = 0
    if re.search("\[.*\]", config["abstract_value"][0][1][0]):
        arrayFlag = 1
    # Using readlines()
    Lines = file1.readlines()
    count = 0
    dec_chk = 0
    # auxFunName = ["min", "max", "concat", "getLength", "unionSet", "intersectionSet", "contains"]
    gValue = "NoGlobal"
    # Strips the newline character
    for line in Lines:
        line = line.replace('ref ', '')
        line = line.replace('global ', '')
        # line = re.sub(r'\/\*.*\*\/', '', line) #not ok for multiple commets in a line
        line = remove_comments(line)
        # line = re.sub('TOP__ANONYMOUS_[a-z0-9]*', 'TOP', line)

        if re.search('TOP__ANONYMOUS_[a-z0-9]*', line) != None:
            line = re.sub('TOP__ANONYMOUS_[a-z0-9]*', 'TOP', line)
            gValue = "TOP"

        elif re.search('ALPHA__ANONYMOUS_[a-z0-9]*', line) != None:
            line = re.sub('ALPHA__ANONYMOUS_[a-z0-9]*', 'ALPHA', line)
            gValue = "ALPHA"

        # now find the returning returning value
        if any(x in line for x in config["abstract_domain"][3]):
            line = line.replace('&', '')
            temp = line.split('(')
            first_part = temp[0]

            temp = temp[1].replace(')', '').strip()  # contain the arguments
            temp = temp.replace('{', '')
            args = temp.split(',')  # contain a list of arguments
            if gValue not in args[-1]:
                ret_args = args[-1].split('_')  # for string domain.. TOP is global
            else:
                ret_args = args[-2].split('_')  # lessThan int out, _ is deleted

            ret_var = '_' + ret_args[-1].replace('{', '')

            arg_str = ""
            if gValue not in args[-1]:
                for i in args[:-1]:
                    arg_str += i + ','
            else:
                for i in args[:-2]:
                    arg_str += i + ','

            # replace return type from void to respective type
            first_part = first_part.replace('void', ret_args[0])

            file2.writelines(first_part + '( ' + arg_str[:-1] + ' ) \n')
            dec_chk = 1


        elif dec_chk == 1:
            file2.writelines("{\n")
            if gValue not in args[-1]:
                retV = args[-1]
            else:
                retV = args[-2]

            dec_chk = 0

            if arrayFlag == 0:
                file2.writelines(" " + retV + ';\n')
            else:
                # incase of array create a dynamic memory location
                tempV = retV.strip()
                tempV = tempV.split(' ')
                size = re.sub('[a-zA-Z\[\]]*', '', tosynthesizeProto[0])  # tempV[0])
                dataType = re.sub('[0-9\[\]\*]*', '', tempV[0])
                if (size == ""):
                    size = "1"
                if "bit" in tosynthesizeProto[0]:
                    file2.writelines(
                        " " + retV + " = bitStruct::create(0, 0, 0);\n")  # (" + dataType+"*)calloc(" + size + ", sizeof(" + dataType+ "));\n")
                else:
                    if "int" == tosynthesizeProto[0] and len(set(tosynthesizeProto[1:])) == 1:
                        file2.writelines(" " + retV + " = 0;\n")
                    else:
                        file2.writelines(
                            " " + retV + " = (" + dataType + "*)calloc(" + size + ", sizeof(" + dataType + "));\n")


            file2.writelines(line)

        elif 'return' in line:
            file2.writelines("  return " + ret_var + ';\n')

        elif any(x in line for x in auxFunName):
            fun_vars = line.replace(';', '').strip().split(',')
            argVars = ""
            for i in range(len(fun_vars) - 1):
                argVars += fun_vars[i] + ', '
            argVars = argVars[:-2]
            file2.writelines(
                ' ' + fun_vars[-1][:-1] + ' = ' + argVars + ');\n')  # fun_vars[0] + ',' + fun_vars[1] + ');\n')

        else:
            file2.writelines(line)

    # close the file
    file1.close()
    file2.close()
    os.system("sed -i  '/AssumptionFailedException()/d' " + tempPath + "f_synth_AFL.cpp")


# this method removes the ref from the sketch code and change the argument position of function call having ref
def removeRef(config):
    tempPath = config["basepath"] + "/temp/"
    file1 = open(tempPath + 'syn_func', 'r')
    file2 = open(tempPath + 'f_synth_old.sk', "a")
    Lines = file1.readlines()

    tosynthesize = list(config["tosynthesize"].keys())[0]
    arrayFlag = 0
    if re.search("\[.*\]", config["abstract_value"][0][1][0]):
        arrayFlag = 1

    count = 0
    dec_chk = 0
    gValue = "NoGlobal"
    # Strips the newline character
    for line in Lines:

        if (tosynthesize == "bitOr" or tosynthesize == "bitAnd" or tosynthesize == "bitXor" or tosynthesize == "multiplication") and (
                "wrappedInterval" in config["dsl"]):
            if "bitWiseTemplateWrapped" in line and "ref" in line:
                justDoNothing = line
            else:
                line = line.replace('ref ', '')
        else:
            line = line.replace('ref ', '')
        line = line.replace('global ', '')
        line = re.sub(r'\/\*.*\*\/', '', line)
        # line = re.sub('TOP__ANONYMOUS_[a-z0-9]*', 'TOP', line)

        if re.search('TOP__ANONYMOUS_[a-z0-9]*', line) != None:
            line = re.sub('TOP__ANONYMOUS_[a-z0-9]*', 'TOP', line)
            gValue = "TOP"

        elif re.search('ALPHA__ANONYMOUS_[a-z0-9]*', line) != None:
            line = re.sub('ALPHA__ANONYMOUS_[a-z0-9]*', 'ALPHA', line)
            gValue = "ALPHA"

        # now find the returning returning value
        if any(x in line for x in config["abstract_domain"][3]):
            temp = line.split('(')
            first_part = temp[0]

            temp = temp[1].replace(')', '').strip()  # contain the arguments
            args = temp.split(',')  # contain a list of arguments
            # print("args in removeref", args)
            if gValue not in args[-1]:
                # print("in top anon")
                ret_args = args[-1].split('_')  # for string domain.. TOP is global
            else:
                ret_args = args[-2].split('_')  # lessThan int out, _ is deleted

            ret_var = '_' + ret_args[-1]

            arg_str = ""
            if gValue not in args[-1]:
                for i in args[:-1]:
                    arg_str += i + ','
            else:
                for i in args[:-2]:
                    arg_str += i + ','

            # replace return type from void to respective type
            first_part = first_part.replace('void', ret_args[0])

            file2.writelines(first_part + '( ' + arg_str[:-1] + ' ) \n')
            dec_chk = 1


        elif '{' in line and dec_chk == 1:
            file2.writelines("{\n")
            if gValue not in args[-1]:
                retV = args[-1]
            else:
                retV = args[-2]

            dec_chk = 0

            if arrayFlag == 0:
                file2.writelines(" " + retV + ';\n')
            else:
                # incase of array create a dynamic memory location
                tempV = retV.strip()
                tempV = tempV.split(' ')
                size = re.sub('[a-zA-Z\[\]]*', '', tempV[0])
                dataType = re.sub('[0-9\[\]]*', '', tempV[0])
                file2.writelines(" " + retV + ';\n')


        elif 'return' in line:
            file2.writelines("  return " + ret_var + ';\n')

        elif any(x in line for x in auxFunName):
            fun_vars = line.replace(';', '').strip().split(',')
            argVars = ""
            for i in range(len(fun_vars) - 1):
                argVars += fun_vars[i] + ', '
            argVars = argVars[:-2]
            file2.writelines(' ' + fun_vars[-1][:-1].replace('{', '').replace('/', '').replace(')',
                                                                                               '') + ' = ' + argVars + ');\n')  # fun_vars[0] + ',' + fun_vars[1] + ');\n')

        else:
            file2.writelines(line)

    # close the file
    file1.close()
    file2.close()
    removeRefCPP(config)
