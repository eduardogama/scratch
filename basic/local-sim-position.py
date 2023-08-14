#!/usr/bin/env python

"""Setting the position of nodes and providing mobility"""
import os
import sys
import math
import json
import random
import threading

import numpy as np

from time import sleep
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from mininet.term import makeTerm




def next_time(rateParameter: float, RAND_MAX: int = 0):
    return -math.log(1.0 - random.random() / (RAND_MAX + 1)) / rateParameter


def DashPlayer(stas: object):

    sleep(5)
    for sta in stas:
        val = next_time(1 / 5.0)
        sleep(val)
        print(sta.wintfs[0].ip, "starting video ... ", sta.wintfs[0].ssid)
        
        makeTerm(sta, cmd='python dash-emulator.py http://143.106.73.17:30001/akamai/bbb_30fps/bbb_30fps.mpd')


def ChromePlayer(stas: object, abrStrategy: str):
    sleep(2)
    for sta in stas:
        val = next_time(1 / 5.0)
        sleep(val)
        print(sta.wintfs[0].ip, "starting video ... ", sta.wintfs[0].ssid)
        makeTerm(
            sta, cmd='google-chrome '
                     '--headless '
                     '--no-sandbox '
                     '--incognito '
                     '--new-window '
                     '--disk-cache-dir=/dev/null '
                     'http://143.106.73.50:30002/samples/ericsson/vod-client.html?userid={}&abrStrategy={}'.format(sta.name, abrStrategy))


def SeleniumPlayer(stas: object, abrStrategy: str, count: str):
    sleep(2)
    for sta in stas:
        val = next_time(1 / 5.0)
        sleep(val)
        print(sta.wintfs[0].ip, "starting video ... ", sta.wintfs[0].ssid)
        
        makeTerm(sta, cmd='python run-player-main.py abrDynamic {} {}'.format(sta.name, count))
        
        
def incoming(stas: object, abrStrategy: str, count: str):
    SeleniumPlayer(stas, abrStrategy, count)


def topology(args):

    """Create a network."""
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    abrStrategy = sys.argv[1] if len(sys.argv) > 1 else "abrDynamic"
    nusers = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    pos1 = sys.argv[3] if len(sys.argv) > 3 else '401.0,1050.0,0.0'
    pos2 = sys.argv[4] if len(sys.argv) > 4 else '1001.0,1050.0,0.0'

    count = sys.argv[5] if len(sys.argv) > 5 else '0'

    nstations = nusers//2
    
    for i in range(1, nstations + 1):
        net.addStation('sta%d' % i, mac='00:00:00:00:00:%02d' % i, position=pos1)

    for i in range(nstations+1, nusers + 1):
        net.addStation('sta%d' % i, mac='00:00:00:00:00:%02d' % i, position=pos2)

    info("*** Creating nodes\n")

    kwargs = {'mode': 'g', 'failMode': 'standalone'}

    e1 = net.addAccessPoint('e1', mac='00:00:00:11:00:01', channel='1',
                            position='400,1050,0', ssid='BS-1', **kwargs)
    e2 = net.addAccessPoint('e2', mac='00:00:00:11:00:02', channel='1',
                            position='1000,1050,0', ssid='BS-2', **kwargs)
    e3 = net.addAccessPoint('e3', mac='00:00:00:11:00:03', channel='1',
                            position='1600,1050,0', ssid='BS-3', **kwargs)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", sL=3, exp=2.8)

    info("*** Configuring nodes\n")
    net.configureWifiNodes()

    net.addLink(e1, e2)
    net.addLink(e2, e3)

    if '-p' not in args:
        net.plotGraph(max_x=2000, max_y=2000)

    info("*** Starting network\n")
    net.build()
    net.addNAT().configDefault()

    e1.start([])
    e2.start([])
    e3.start([])

    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)

