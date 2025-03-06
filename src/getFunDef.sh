#!/bin/sh
# $1 = file name
# $2 = function name
awk '
BEGIN { state = 0; }
$0 ~ /^(void|int|bit| int| bit| int )[a-zA-Z0-9\[\]\*\+ ]*'$2'[ ]*\(/ { state = 1; }
        { if (state == 1) print; }
$0 ~ /^}/ { if (state) state = 2; }
' $1
