#!/usr/bin/env python

'Setting position of the nodes'

import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from mn_wifi.node import UserAP


def topology(args):

    net = Mininet_wifi(link=wmediumd, accessPoint=UserAP, 
                       wmediumd_mode=interference)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1',
                             failMode="standalone", mac='00:00:00:00:00:01',
                             position='50,50,0')
    net.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8',
                   position='30,60,0')
    net.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.2/8',
                   position='70,30,0')
    
    h1 = net.addHost('h1', ip='10.0.0.4/8', mac='00:00:00:00:00:09')
    # d1 = net.addDocker('d2', ip='10.0.0.3', dimage="eduardogama/dashcache:latest")

    info("*** Configuring propagation model\n")
    # net.setPropagationModel(model="logDistance", exp=4.5)
    net.setPropagationModel(model="friis", sL=3)

    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Creating links\n")
    net.addLink(ap1, h1)
    # net.addLink(ap1, d1)

    if '-p' not in args:
        net.plotGraph(max_x=3500, max_y=3500)

    info("*** Starting network\n")
    net.build()

    net.addNAT().configDefault()
    
    ap1.start([])
    h1.start()

    # result = h1.cmd("docker run -p 30001:30001 -t eduardogama/dashcache:latest")
    # print(result)
    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
