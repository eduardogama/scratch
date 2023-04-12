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

    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)
    

    info('*** Adding controller\n')

    info('*** Adding docker containers\n')
    # d1 = net.addDocker('d1', ip='10.0.0.4/8', dcmd="python app.py", 
    #                    mac="00:00:00:00:00:05",
    #                    dimage="eduardogama/dashcache:latest",
    #                    ports=[80], port_bindings={80: 3000})
    info("*** Creating nodes\n")

    kwargs = {'mode': 'g', 'failMode': 'standalone'}
    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', channel='1', mac='00:00:00:00:00:01', position='50,50,0', **kwargs)

    net.addStation('sta1', mac='00:00:00:00:00:02', position='30,60,0')
    net.addStation('sta2', mac='00:00:00:00:00:03', position='70,30,0')
    
    h1 = net.addHost('h1', mac="00:00:00:00:00:05")

    info("*** Configuring propagation model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)
    # net.setPropagationModel(model="friis", sL=3)

    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Creating links\n")
    net.addLink(ap1, h1)

    if '-p' not in args:
        net.plotGraph(max_x=500, max_y=500)

    info("*** Starting network\n")
    net.build()

    net.addNAT().configDefault()
    
    ap1.start([])
    # result = h1.cmd("docker run -d -p 80:80 -t eduardogama/dashcache:latest")
    # print(result) q
    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
