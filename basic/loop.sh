#!/bin/bash
for i in 1 2 3 4 5 6 7 8 9 10; do
  curl -X POST 143.106.73.50:30700/collect/handover -H 'Content-Type: application/json' -d $(jo userName=user$i bsName=BS-1 ip=172.18.37.105)
  python selenium-start.py user$i &
done

sleep 2

for i in 11 12 13 14 15 16 17 18 19 20; do
  curl -X POST 143.106.73.50:30700/collect/handover -H 'Content-Type: application/json' -d $(jo userName=user$i bsName=BS-3 ip=172.18.37.105)
  python selenium-start.py user$i &
done

sleep 2

for i in 21 22 23 24 25; do
  curl -X POST 143.106.73.50:30700/collect/handover -H 'Content-Type: application/json' -d $(jo userName=user$i bsName=BS-5 ip=172.18.37.105)
  python selenium-start.py user$i &
done
