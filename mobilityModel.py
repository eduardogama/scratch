#!/usr/bin/env python

'Setting the position of Nodes and providing mobility using mobility models'
import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi


def topology(args):
    "Create a network."
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.2/8', min_x=10, max_x=100, min_y=20, max_y=30, min_v=5, max_v=10)
    
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1', failMode="standalone", position='50,50,0')

    net.setMobilityModel(time=0, model='RandomDirection', max_x=100, max_y=100, seed=20)


    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Starting network\n")
    net.plotGraph(max_x=500, max_y=500)
    net.build()
    ap1.start([])

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)