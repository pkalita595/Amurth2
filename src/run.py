import sys
import os

benchmark = {
    "oe":{
        "increment": "config/reduced/evenOdd/reducedIncrementNew.json",
        "add"      : "config/reduced/evenOdd/reducedAddNew.json",
        "sub"      : "config/reduced/evenOdd/reducedSubBest.json",
        "abs"      :"config/reduced/evenOdd/reducedAbsBest.json",
    },    
    "jsai":{
        "concat"   : "config/reduced/jsai/concatCSNew.json",
        "contains" : "config/reduced/jsai/containsNew.json",
        "toLower"  : "config/reduced/jsai/toLowerNew.json",
        "toUpper"  : "config/reduced/jsai/toUpperNew.json",
        "charAt"   : "config/reduced/jsai/charAt.json",
        "trim"     : "config/reduced/jsai/trimNew.json"
    },
    "safe" : {
        "concat"   : "config/reduced/jsai/concat.json",
        "contains" : "config/reduced/jsai/contains.json",
        "toLower"  : "config/reduced/jsai/toLowerNew.json",
        "toUpper"  : "config/reduced/jsai/toUpperNew.json",
        "charAt"   : "config/reduced/jsai/charAt.json",
        "trim"     : "config/reduced/jsai/trimNew.json",
    }
}



dom = sys.argv[1]
op = sys.argv[2]

if dom not in benchmark.keys():
    print("Enter a valid domain id as shown in the readme.")
    exit()
if op not in benchmark[dom].keys():
    print("Entered a wrong operation for the given domain. Please enter a valid operation.")
    exit()

os.system("bash single_ex.sh " +  benchmark[dom][op])
