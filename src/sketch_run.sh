#!/bin/bash

#$1 for sketch file
#$2 for toolpath
param=$1
fileName="${param/.sk/}"

rm $2/temp/hole.xml
trap "exit" INT
# create sketch dir in temp if doesn't exist
echo "SKETCH start"
start=$(date +%s.%N)
trap "exit" INT

#for safe domain
#sketch --slv-parallel --slv-p-cpus 6 --fe-output-xml $2temp/hole.xml --fe-output-test  -p cleanup  --fe-output-dir $2temp/sketch/  $1 > $2temp/result_file 2>&1

sketch --fe-output-xml $2temp/hole.xml --fe-output-test  -p cleanup  --fe-output-dir $2temp/sketch/  $1 > $2temp/result_file 2>&1

# for interval
#sketch --slv-nativeints  --fe-output-xml $2temp/hole.xml --fe-output-test  -p cleanup  --fe-output-dir $2temp/sketch/  $1 > $2temp/result_file 2>&1

# sketch --bnd-int-range 200  --fe-output-xml $2temp/hole.xml --slv-synth MINI --fe-output-test  -p cleanup  --fe-output-dir $2temp/sketch/  $1 > $2temp/result_file 2>&1

# sketch --bnd-int-range 100 --slv-parallel --slv-p-cpus 8 --fe-output-xml $2temp/hole.xml --slv-synth MINI --fe-output-test  -p cleanup  --fe-output-dir $2temp/sketch/  $1 > $2temp/result_file 2>&1

# sketch   --slv-parallel --slv-p-cpus 6  --fe-output-xml $2temp/hole.xml --fe-output-test  -p cleanup  --fe-output-dir $2temp/sketch/  $1 > $2temp/result_file 2>&1

echo "SKETCH end" $?
trap "exit" INT
grep -s "Must be SPARSE\|assert (0); //This function should never be called. Will cause ASSERTION CAN NOT BE SATISFIED" $2temp/result_file

if [ $? == 0 ]
then
    echo "Doing again"
    start=$(date +%s.%N)
    sketch --bnd-int-range 32 --fe-output-xml $2temp/hole.xml --fe-output-test  -p cleanup  --fe-output-dir $2temp/sketch/  $1 > $2temp/result_file 2>&1
fi

duration=$(echo "$(date +%s.%N) - $start" | bc)

sed -i '/^\[SATBackend\]/d' $2temp/result_file
sed -i '/^=== parallel trial/d' $2temp/result_file


grep -s "E[rR][rR][oO][rR]" $2temp/result_file

if [ $? == 0 ]
then
  echo "UNSAT"> $2temp/sketch_result
  echo $duration >> $2temp/sketch_result
  exit
fi

echo "SAT" > $2temp/sketch_result
echo $duration >> $2temp/sketch_result

cp $fileName".cpp" $2temp/result_file_cpp

exit

echo "" > "sketchHole.txt"
g++ -I $2/include/ $fileName"_test.cpp" $fileName".cpp" -o ./holeExe
./holeExe
sed '/^$/d' -i  "sketchHole.txt"

