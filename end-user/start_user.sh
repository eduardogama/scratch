#!/bin/bash



if [ $# -lt 3 ]
then
    echo "Invalid interface"
    echo "start_user.sh <user id> <net interface> <startup delay>"
    return 1
fi

iuser=$1
iname=$2
istart=$3

adduser --gecos "" --disabled-password $iuser

sleep $istart

#iptables -A OUTPUT -t mangle -m owner --uid $user -j MARK --set-mark $1

runuser -l $user -c "mkdir -p /usr/workspace/.browser/$iuser"
runuser -l $user -c "python3 /usr/workspace/run-player-main.py $iuser"

