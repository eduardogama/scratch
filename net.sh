MAC_ROKU1=00:00:00:11:00:01
MAC_ROKU2=00:00:00:11:00:04
 
DEV=nat0-eth0
TC=$(which tc)
TCF="${TC} filter add dev $DEV parent 1: protocol ip prio 5 u32 match u16 0x0800 0xFFFF at -2"
 
filter_mac() {
 
  M0=$(echo $1 | cut -d : -f 1)$(echo $1 | cut -d : -f 2)
  M1=$(echo $1 | cut -d : -f 3)$(echo $1 | cut -d : -f 4)
  M2=$(echo $1 | cut -d : -f 5)$(echo $1 | cut -d : -f 6)
 
  $TCF match u16 0x${M2} 0xFFFF at -4 match u32 0x${M0}${M1} 0xFFFFFFFF at -8 flowid $2
  $TCF match u32 0x${M1}${M2} 0xFFFFFFFF at -12 match u16 0x${M0} 0xFFFF at -14 flowid $2
}
 
insmod sch_htb 2> /dev/null



filter_mac $MAC_ROKU1 1:1 
filter_mac $MAC_ROKU2 1:2