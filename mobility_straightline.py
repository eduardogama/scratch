#!/usr/bin/env python

'Setting the position of nodes and providing mobility'

import sys

import numpy as np

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from mininet.term import makeTerm


def topology(args):
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       wmediumd_mode=interference)

    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01')
    info("*** Creating nodes\n")

    kwargs = {'mode': 'g', 'failMode': 'standalone'}

    e1 = net.addAccessPoint('e1', mac='00:00:00:11:00:01', channel='1',
                            position='400,1050,0', ssid='ssid-ap1', **kwargs)
    e2 = net.addAccessPoint('e2', mac='00:00:00:11:00:02', channel='1',
                            position='1000,1050,0', ssid='ssid-ap2', **kwargs)
    e3 = net.addAccessPoint('e3', mac='00:00:00:11:00:03', channel='1',
                            position='1600,1050,0', ssid='ssid-ap3', **kwargs)
    e4 = net.addAccessPoint('e4', mac='00:00:00:11:00:04', channel='1',
                            position='2200,1050,0', ssid='ssid-ap4', **kwargs)
    e5 = net.addAccessPoint('e5', mac='00:00:00:11:00:05', channel='1',
                            position='2800,1050,0', ssid='ssid-ap5', **kwargs)
    e6 = net.addAccessPoint('e6', mac='00:00:00:11:00:06', channel='1',
                            position='3400,1050,0', ssid='ssid-ap6', **kwargs)
    e7 = net.addAccessPoint('e7', mac='00:00:00:11:00:07', channel='1',
                            position='4000,1050,0', ssid='ssid-ap7', **kwargs)
    e8 = net.addAccessPoint('e8', mac='00:00:00:11:00:08', channel='1',
                            position='4600,1050,0', ssid='ssid-ap8', **kwargs)
    e9 = net.addAccessPoint('e9', mac='00:00:00:11:00:09', channel='1',
                            position='5200,1050,0', ssid='ssid-ap9', **kwargs)
    e10 = net.addAccessPoint('e10', mac='00:00:00:11:00:10', channel='1',
                            position='5800,1050,0', ssid='ssid-ap10', **kwargs)

    # c1 = net.addController('c1')

    h1 = net.addHost('h1', mac="00:00:00:00:00:05")

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", sL=3, exp=2.8)

    info("*** Configuring nodes\n")
    net.configureNodes()

    net.addLink(e1, e2)
    net.addLink(e2, e3)
    net.addLink(e3, e4)
    net.addLink(e4, e5)
    net.addLink(e5, e6)
    net.addLink(e6, e7)
    net.addLink(e8, e9)
    net.addLink(e9, e10)

    net.addLink(e1, h1)


    net.startMobility(time=0)

    p1, p2, p3, p4 = {}, {}, {}, {}
    if '-c' not in args:
        p1 = {'position': '80.0,1050.0,0.0'}
        p2 = {'position': '5800.0,1050.0,0.0'}
        
    net.mobility(sta1, 'start', time=1, **p1)
    net.mobility(sta1, 'stop', time=100, **p2)
    net.stopMobility(time=601)


    if '-p' not in args:
        net.plotGraph(max_x=6500, max_y=6500)

    info("*** Starting network\n")
    net.build()

    net.addNAT().configDefault()

    e1.start([])
    e2.start([])
    e3.start([])
    e4.start([])
    e5.start([])
    e6.start([])
    e7.start([])
    e8.start([])
    e9.start([])
    e10.start([])

    # stations = np.array([sta1, sta2])
    stations = np.array([sta1])

    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
