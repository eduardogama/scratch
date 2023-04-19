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
from mininet.term import makeTerm


def nextTime(rateParameter, RAND_MAX=0):
    return -math.log(1.0 - random.random()/(RAND_MAX + 1)) / rateParameter


def incoming(stas):

    for sta in stas:
        val = nextTime(1/5.0)
        sleep(val)
        print(sta.wintfs[0].ip, "starting video ... ", sta.wintfs[0].ssid)
        makeTerm(
            sta, cmd='google-chrome --no-first-run '\
                '--disable-gesture-requirement-for-media-playback '\
                '--no-sandbox '\
                '--disable-gpu '\
                '--disable-plugins '\
                '--incognito '\
                '--new-window '\
                'http://143.106.73.50:30002/samples/ericsson/vod-1.html')
    

def monitoring(stas):
    # Monitor the connectivity of the station
    prev_ap = []

    while True:
        for sta in stas:
            connected_ap = sta.wintfs[0].ssid
            print('Connected to:', connected_ap)

            # Check if the station connects to a different access point
            if connected_ap != prev_ap:
                print('[', sta.wintfs[0].ip, '] Access point changed from',
                      prev_ap, 'to', connected_ap, '! ')
                prev_ap = connected_ap

            # Wait for a few seconds before checking the connectivity again
            sleep(2)


def topology(args):
    "Create a network."
    net = Mininet_wifi(controller=Controller, link=wmediumd,
                       wmediumd_mode=interference)

    stations = []
    for i in range(1, 6):
        sta = net.addStation('sta'+ str(i), mac='00:00:00:00:00:0'+ str(i),
                            min_x=100, max_x=2000, min_y=100, max_y=1400, min_v=10, max_v=20)

        stations.append(sta)

    for i in range(1, 6):
        sta = net.addStation('sta1'+ str(i), mac='00:00:00:00:00:1'+ str(i),
                            min_x=100, max_x=2000, min_y=100, max_y=1400, min_v=3, max_v=5)

        stations.append(sta)

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

    net.setMobilityModel(time=0, model='RandomDirection',
                         max_x=2000, max_y=1200, seed=20)

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

    # makeTerm(sta1, cmd='google-chrome --no-first-run --disable-gesture-requirement-for-media-playback --no-sandbox http://143.106.73.50:30002/samples/ericsson/vod-1.html')

    # makeTerm(sta2, cmd="python end-user/run-player-main.py")
    # makeTerm(sta2, cmd="bash -c 'python end-user/run-player-main.py'")

    # stations = np.array([sta1, sta2])
    stations = np.array(stations)

    threading.Thread(target=monitoring, args=(stations,)).start()
    threading.Thread(target=incoming, args=(stations,)).start()

    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
