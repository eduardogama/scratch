#!/bin/bash


## Function that will get executed when the user presses Ctrl+C
#function handler(){
#    echo "Processing the Ctrl+C"
#    echo "Parameters of experiment "
#}

## Assign the handler function to the SIGINT signal
#trap handler SIGINT


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
            for abrStrategy in "abrDynamic" "abrThroughput" "abrBola" "abrL2A" "abrLoLP";
            do
                # Simulation progress
                echo "$count $abrStrategy $nusers ${groupOnePosition[$i]} ${groupTwoPosition[$i]}" >> $filename
                
                # Download Chrome
                python download-chrome.py
                
                # Start Simulation
                python position.py $abrStrategy $nusers ${groupOnePosition[$i]} ${groupTwoPosition[$i]} $count
                
                # Cleanup
                mn -c
              
                # Reset caches 
                curl http://143.106.73.17:30001/reset?capacity=100
                
                # Release users connections
                curl "http://143.106.73.50:30500/releaseServers"
                
                sleep 90
                count=$((count+1))
            done
        done
    done
fi
