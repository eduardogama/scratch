#!/usr/bin/env python

"""Setting the position of nodes and providing mobility"""

import sys
import os
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


def incoming(stas: object):
    for sta in stas:
        val = next_time(1 / 5.0)
        sleep(val)
        print(sta.wintfs[0].ip, "starting video ... ", sta.wintfs[0].ssid)
        makeTerm(
            sta, cmd='google-chrome '
                     '--disable-application-cache '
                     '--media-cache-size=1 '
                     '--disk-cache-dir=/dev/null '
                     '--no-sandbox '
                     '--disable-gpu '
                     '--incognito '
                     '--new-window '
                     'http://143.106.73.50:30002/samples/ericsson/vod-client.html?userid={}'.format(sta.name))


def monitoring(stas):
    # Monitor the connectivity of the station
    prev_ap = np.array([None for i in enumerate(stas)])

    while True:
        for i, sta in enumerate(stas):
            connected_ap = sta.wintfs[0].ssid

            if connected_ap != prev_ap[i]:
                print(
                    json.dumps(
                        {"userName": sta.name, "bsName": connected_ap, "ip": sta.wintfs[0].ip})
                )

                os.system(
                    "curl -X POST 143.106.73.50:30700/collect/handover -H 'Content-Type: application/json' -d $(jo "
                    "userName={} bsName={} ip={})"
                    .format(sta.name, connected_ap, sta.wintfs[0].ip))

                prev_ap[i] = connected_ap

            sleep(2)


def topology(args):
    """Create a network."""
    net = Mininet_wifi()

    nusers = 3

    for i in range(1, nusers + 1):
        net.addStation('sta%d' % i, mac='00:00:00:00:00:%02d' % i)

    info("*** Creating nodes\n")

    kwargs = {'mode': 'g', 'failMode': 'standalone'}

    e1 = net.addAccessPoint('e1', mac='00:00:00:11:00:01', channel='1',
                            position='400,1050,0', ssid='BS-1', **kwargs)
    e2 = net.addAccessPoint('e2', mac='00:00:00:11:00:02', channel='1',
                            position='1000,1050,0', ssid='BS-2', **kwargs)
    e3 = net.addAccessPoint('e3', mac='00:00:00:11:00:03', channel='1',
                            position='1600,1050,0', ssid='BS-3', **kwargs)
    e4 = net.addAccessPoint('e4', mac='00:00:00:11:00:04', channel='1',
                            position='2200,1050,0', ssid='BS-4', **kwargs)
    e5 = net.addAccessPoint('e5', mac='00:00:00:11:00:05', channel='1',
                            position='2800,1050,0', ssid='BS-5', **kwargs)
    e6 = net.addAccessPoint('e6', mac='00:00:00:11:00:06', channel='1',
                            position='3400,1050,0', ssid='BS-6', **kwargs)
    e7 = net.addAccessPoint('e7', mac='00:00:00:11:00:07', channel='1',
                            position='4000,1050,0', ssid='BS-7', **kwargs)
    e8 = net.addAccessPoint('e8', mac='00:00:00:11:00:08', channel='1',
                            position='4600,1050,0', ssid='BS-8', **kwargs)
    e9 = net.addAccessPoint('e9', mac='00:00:00:11:00:09', channel='1',
                            position='5200,1050,0', ssid='BS-9', **kwargs)
    e10 = net.addAccessPoint('e10', mac='00:00:00:11:00:10', channel='1',
                             position='5800,1050,0', ssid='BS-10', **kwargs)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", sL=3, exp=2.8)

    info("*** Configuring nodes\n")
    net.configureWifiNodes()

    net.addLink(e1, e2)
    net.addLink(e2, e3)
    net.addLink(e3, e4)
    net.addLink(e4, e5)
    net.addLink(e5, e6)
    net.addLink(e6, e7)
    net.addLink(e7, e8)
    net.addLink(e8, e9)
    net.addLink(e9, e10)

    p1, p2 = {}, {}
    if '-c' not in args:
        p1 = {'position': '100.0,1050.0,0.0'}
        p2 = {'position': '6000.0,1050.0,0.0'}

    for sta in net.stations:
        sta.coord = ['100.0,1050.0,0.0', '6000.0,1050.0,0.0']

    net.startMobility(time=0)

    for sta in net.stations:
        net.mobility(sta, 'start', time=1, **p1)
        net.mobility(sta, 'stop', time=200, **p2)

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
    # stations = np.array(net.stations)
    # threading.Thread(target=monitoring, args=(stations,)).start()
    # threading.Thread(target=incoming, args=(stations,)).start()

    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
