#!/bin/bash


if [ $# -lt 1 ]
then
    echo "Invalid input"
    echo "strat-simulations.sh <# of users>"
    return 1
else
    nusers=$1
    groupOnePosition=('401.0,1050,0' '500.0,1050,0' '600.0,1050,0' '700.0,1050,0')
    groupTwoPosition=('1001.0,1050,0' '1100.0,1050,0' '1200.0,1050,0' '1300.0,1050,0')

    len=${#groupOnePosition[@]}

    filename=sim.$(date "+%Y.%m.%d-%H.%M.%S")
    
    
    count=0

    for k in $(seq 1 5);
    do
        for i in $(seq 0 $((len-1)));
        do
            for abrStrategy in "abrThroughput" "abrDynamic" "abrBola";
            do
                # Simulation progress
                echo "$count $abrStrategy $nusers ${groupOnePosition[$i]} ${groupOnePosition[$i]}" >> $filename
                
                # Start Simulation
                python position.py $abrStrategy $nusers ${groupOnePosition[$i]} ${groupOnePosition[$i]} $count
                
                # Cleanup
                mn -c
              
                # Reset caches 
                curl http://143.106.73.17:30001/reset?capacity=100
                
                sleep 60
                count=$((count+1))
            done
        done
    done
fi
