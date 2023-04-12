#!/bin/bash

i=0
time=`python3 poisson.py $1`

for t in $time
do
    mkdir -p .browser/user-$i 
    python3 run-player-main.py $i &
    
    i=$((i+1))
    sleep $t
done


