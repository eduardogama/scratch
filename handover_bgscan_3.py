#!/usr/bin/python

import os
import sys

from mininet.node import Controller
from mn_wifi.node import UserAP
from mininet.log import setLogLevel, info
from mn_wifi.bmv2 import P4AP, P4Switch
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.net import Mininet_wifi
from mininet.term import makeTerm
from mn_wifi.wmediumdConnector import interference


def topology():
    'Create a network.'
    net = Mininet_wifi(controller=Controller, 
        link=wmediumd, wmediumd_mode=interference)

    info('*** Adding stations\n')
    sta1 = net.addStation('sta1', ip='10.0.0.1', mac="00:00:00:00:00:01")


    ap1 = net.addAccessPoint('ap1', mac="00:00:00:00:00:03", ssid='handover', channel=1, position='40,40,0')
    ap2 = net.addAccessPoint('ap2', mac="00:00:00:00:00:04", ssid='handover', channel=1, position='80,40,0')

    info("*** Configuring propagation model\n")
    # net.setPropagationModel(model="logDistance", exp=4)

    net.configureWifiNodes()

    info("*** Adding links\n")
    net.addLink(ap1, ap2)

    net.plotGraph(max_x=300, max_y=300)

    net.startMobility(time=0)
    net.mobility(sta1, 'start', time=1, position='10,30,0')
    net.mobility(sta1, 'stop', time=59, position='125,30,0')
    net.stopMobility(time=6000)

    info('*** Starting network\n')
    net.build()
    net.addNAT().configDefault()

    ap1.start([])
    ap2.start([])

    ap1.setTxPower(-10)
    ap2.setTxPower(-10)

    # ap1.cmd('iw dev ap1-wlan1 interface add mon1 type monitor')
    # ap2.cmd('iw dev ap2-wlan1 interface add mon2 type monitor')
    # ap1.cmd('ip link set mon1 up')
    # ap2.cmd('ip link set mon2 up')
 	
    # makeTerm(ap1, cmd="bash -c 'python handover-controller.py mon1 3;'")
    # makeTerm(ap2, cmd="bash -c 'python handover-controller.py mon2 4;'")
    # makeTerm(sta1, cmd="bash -c 'ping 10.0.0.2;'")

    info('*** Running CLI\n')
    CLI(net)

    os.system('pkill -f -9 \"xterm\"')

    info('*** Stopping network\n')
    net.stop()
    

if __name__ == '__main__':
    setLogLevel('info')
    topology()
