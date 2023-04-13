#!/usr/bin/env python

'Setting the position of nodes and providing mobility'

import sys

from time import sleep

from mn_wifi.node import UserAP
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from mininet.term import makeTerm


def topology(args):
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd, accessPoint=UserAP,
                       wmediumd_mode=interference)

    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', range=10,
                          min_x=100, max_x=2000, min_y=100, max_y=1400, min_v=10, max_v=0)
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:02', range=10,
                          min_x=100, max_x=2000, min_y=100, max_y=1400, min_v=3, max_v=5)
    # sta3 = net.addStation('sta3', mac='00:00:00:00:00:03', min_x=100, max_x=700, min_y=50, max_y=450, min_v=20, max_v=30)
    # sta4 = net.addStation('sta4', mac='00:00:00:00:00:04', min_x=100, max_x=700, min_y=50, max_y=450, min_v=20, max_v=30)
    # sta5 = net.addStation('sta5', mac='00:00:00:00:00:05', min_x=100, max_x=700, min_y=50, max_y=450, min_v=20, max_v=30)

    info("*** Creating nodes\n")

    kwargs = {'mode': 'g', 'failMode': 'standalone'}

    e1 = net.addAccessPoint('e1', mac='00:00:00:11:00:01', channel='1', 
                            position='400,1050,0', ssid='ssid-ap1', **kwargs)
    e2 = net.addAccessPoint('e2', mac='00:00:00:11:00:02', channel='1', 
                            position='1000,1050,0', ssid='ssid-ap2', **kwargs)
    e3 = net.addAccessPoint('e3', mac='00:00:00:11:00:03', channel='1',
                            position='1600,1050,0', ssid='ssid-ap3', **kwargs)
    e4 = net.addAccessPoint('e4', mac='00:00:00:11:00:04', channel='1',
                            position='400,450,0', ssid='ssid-ap4', **kwargs)
    e5 = net.addAccessPoint('e5', mac='00:00:00:11:00:05', channel='1',
                            position='1000,450,0', ssid='ssid-ap5', **kwargs)
    e6 = net.addAccessPoint('e6', mac='00:00:00:11:00:06', channel='1',
                            position='1600,450,0', ssid='ssid-ap6', **kwargs)
    
    # c1 = net.addController('c1')

    h1 = net.addHost('h1', mac="00:00:00:00:00:05")

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=2.8)

    info("*** Configuring nodes\n")
    net.configureNodes()
    
    net.addLink(e1, e2)
    net.addLink(e2, e3)
    net.addLink(e3, e4)
    net.addLink(e4, e5)
    net.addLink(e5, e6)

    net.addLink(e1, h1)

    net.setMobilityModel(time=10, model='RandomDirection', max_x=2000, max_y=1200, seed=20)


    net.plotGraph(max_x=2000, max_y=1600)

    info("*** Starting network\n")
    net.build()

    net.addNAT().configDefault()

    e1.start([])
    e2.start([])
    e3.start([])
    e4.start([])
    e5.start([])
    e6.start([])
    
    # sta1.cmd('google-chrome --no-sandbox http://143.106.73.50:30002/samples/ericsson/vod-1.html')
    # sta1.cmd('python end-user/run-player-main.py')
    # makeTerm(sta1, cmd="python end-user/run-player-main-2.py")
    # sleep(2)
    # makeTerm(sta1, cmd='google-chrome --no-sandbox http://143.106.73.50:30002/samples/ericsson/vod-1.html')

    # makeTerm(sta2, cmd="python end-user/run-player-main.py")
    # makeTerm(sta2, cmd="bash -c 'python end-user/run-player-main.py'")

    info("*** Running CLI\n")
    CLI(net)


    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
