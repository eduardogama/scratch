#!/usr/bin/env python


import sys

from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI



def topology(args):
    info("Creating network \n")

    net = Mininet_wifi()

    info("*** Creating nodes\n")
    
    sta1_args, sta2_args, sta3_args = {}, {}, {}
    sta1_args['position'], sta2_args['position'], sta3_args['position'] = '20,20,0', '60,20,0', '100,20,0'

    sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', **sta1_args)

    
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', channel='1', position='15,30,0')
    ap2 = net.addAccessPoint('ap2', ssid='ssid-ap2', channel='6', position='55,30,0')
    ap3 = net.addAccessPoint('ap3', ssid='ssid-ap3', channel='5', position='95,30,0')

    c1 = net.addController('c1')

    net.setPropagationModel(model="logDistance", exp=5)


    info("Configuring Nodes")
    net.configureNodes()

    info("*** Creating links\n")
    net.addLink(ap1, ap2)
    net.addLink(ap2, ap3)

    net.plotGraph(max_x=100, max_y=100)


    net.startMobility(time=0)
    net.mobility(sta1, 'start', time=1, position='10,20,0')
    net.mobility(sta1, 'stop', time=20, position='100,20,0')

    info("Starting Network\n")
    net.build()

    c1.start()

    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])

    info("Running CLI \n")
    CLI(net)


    info("Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel("info")
    topology(sys.argv)