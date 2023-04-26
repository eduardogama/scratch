#!/usr/bin/env python

'Setting the position of nodes and providing mobility'

import sys
import math
import random
import threading

from time import sleep
import numpy as np

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference



matrix = [
    [0, 1, 0, 1, 0, 0],
    [1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1],
    [0, 0, 1, 0, 1, 0]
]

def topology(args):
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       wmediumd_mode=interference)

    stations = []

    for i in range(1, 2):

        x, y = random.uniform(250, 550), random.uniform(900,1200)

        sta = net.addStation('sta' + str(i), mac='00:00:00:00:00:%02d'%(i), 
                             position='{},{},0'.format(250, 1050))
        stations.append(sta)

    info("*** Creating nodes\n")

    kwargs = {'mode': 'g', 'failMode': 'standalone'}

    e1 = net.addAccessPoint('BS-1', mac='00:00:00:11:00:01', channel='1',
                            position='400,1050,0', ssid='BS-1', **kwargs)
    e2 = net.addAccessPoint('BS-2', mac='00:00:00:11:00:02', channel='1',
                            position='1000,1050,0', ssid='BS-2', **kwargs)
    e3 = net.addAccessPoint('BS-3', mac='00:00:00:11:00:03', channel='1',
                            position='1600,1050,0', ssid='BS-3', **kwargs)
    e4 = net.addAccessPoint('BS-4', mac='00:00:00:11:00:04', channel='1',
                            position='400,450,0', ssid='BS-4', **kwargs)
    e5 = net.addAccessPoint('BS-5', mac='00:00:00:11:00:05', channel='1',
                            position='1000,450,0', ssid='BS-5', **kwargs)
    e6 = net.addAccessPoint('BS-6', mac='00:00:00:11:00:06', channel='1',
                            position='1600,450,0', ssid='BS-6', **kwargs)


    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", sL=8, exp=2.8)

    info("*** Configuring nodes\n")
    net.configureNodes()

    net.addLink(e1, e2)
    net.addLink(e2, e3)
    net.addLink(e3, e4)
    net.addLink(e4, e5)
    net.addLink(e5, e6)


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


    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
