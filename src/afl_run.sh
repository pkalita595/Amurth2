#!/bin/bash
    # $1: tool path

    #TODO: Have to check where this crash will appear
    crash_path="crash"
    trap "exit" INT
    afl_path=$1/afl
    rm $crash_path
    rm posex.txt
 
    sed -i '/AssumptionFailedException()/d'  $1/temp/f_synth_AFL.cpp
   
    #compile the program with afl-g++
    $afl_path/afl-g++ $1/temp/aflTest.cc -I $1/include/ -L $1/external_lib -lmath -lm -g -w -o  $1/temp/aflTest   > /dev/null  2>&1  #-L$1/external_lib/ $2
    #$1/temp/f_synth_old.c
    if [ $? -ne 0 ];
    then
        echo "Compile Error: Aborting"
        echo "abort"> $1/temp/afl_result
        exit
    fi


    timeout --preserve-status 1000 $afl_path/afl-fuzz -i $1/temp/input/ -o output/ $1/temp/aflTest

    ls $crash_path

    if [ $? -ne 0 ];
    then
        echo "timeout"> $1/temp/afl_result
        exit
    fi

    echo "success" > $1/temp/afl_result
    cp $crash_path $1/temp/crash
    exit

    #TODO: have to check how to process the afl inputs
    g++ -o process_crash process_crash.cpp

    if [ $? -ne 0 ];
    then
        echo "compilation error"
        exit
    fi

    ./process_crash < $crash_path
    
    
