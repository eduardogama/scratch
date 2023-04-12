#!/bin/bash

iname=$(ip addr show | awk '/inet.*brd/{print $NF}')

tc filter del dev $iname
tc filter add dev $iname protocol all parent 1:0 prio 1 u32 match ip dst 143.106.73.17 flowid 1:1
tc filter add dev $iname protocol all parent 1:0 prio 2 u32 match ip dst 143.106.73.23 flowid 1:2
tc filter add dev $iname protocol all parent 1:0 prio 2 u32 match ip dst 143.106.73.19 flowid 1:2


