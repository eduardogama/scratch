#!/usr/bin/env python

'Example for Handover'

import sys

from mn_wifi.node import UserAP
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.wmediumdConnector import interference

from mininet.log import setLogLevel, info
from mininet.node import Controller


def topology(args):
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    kwargs = {'mode': 'g', 'failMode': 'standalone'}

    sta1_args, sta2_args = {}, {}
    if '-s' in args:
        sta1_args['position'], sta2_args['position'] = '20,30,0', '60,30,0'

    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', **sta1_args)
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:02', **sta2_args)
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mac='00:00:00:11:00:01', channel='1', position='15,30,0', **kwargs)
    ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', mac='00:00:00:11:00:02', channel='1', position='55,30,0', **kwargs)
    c1 = net.addController('c1')

    net.setPropagationModel(model="logDistance", exp=5)

    info("*** Configuring nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(ap1, ap2)

    if '-p' not in args:
        net.plotGraph(max_x=100, max_y=100)

    if '-s' not in args:
        net.startMobility(time=0)
        net.mobility(sta1, 'start', time=1, position='10,30,0')
        net.mobility(sta2, 'start', time=2, position='10,40,0')
        net.mobility(sta1, 'stop', time=30, position='60,30,0')
        net.mobility(sta2, 'stop', time=30, position='25,40,0')
        net.stopMobility(time=31)

    info("*** Starting network\n")
    net.build()

    net.addNAT().configDefault()

    c1.start()
    ap1.start([c1])
    ap2.start([c1])

    net.start()

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)