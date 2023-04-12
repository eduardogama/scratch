#!/bin/bash


if [ -z "$1" ]
then
    iname=$(ip addr show | awk '/inet.*brd/{print $NF}')        
else
    iname=$1
fi


tc qdisc del dev $iname root
tc qdisc add dev $iname root handle 1: prio

tc qdisc add dev $iname parent 1:1 handle 10: netem loss 0.09% rate 100mbps
tc qdisc add dev $iname parent 1:2 handle 20: netem delay 50ms loss 0.09% rate 100mbps

# The user starts from edge node 1 
#sh edge1.sh


#tc filter add dev $iname protocol all parent 1:0 prio 4 u32 match ip dst 143.106.73.50 flowid 1:4
#tc filter add dev $iname protocol all parent 1:0 prio 4 u32 match ip dst 143.106.73.19 flowid 1:4
