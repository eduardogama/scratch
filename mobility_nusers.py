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
import os

import json


def nextTime(rateParameter, RAND_MAX=0):
    return -math.log(1.0 - random.random()/(RAND_MAX + 1)) / rateParameter


def incoming(stas):

    for sta in stas:
        val = nextTime(1/5.0)
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
                    "curl -X POST 143.106.73.50:30700/collect/handover -H 'Content-Type: application/json' -d $(jo userName={} bsName={} ip={})"
                    .format(sta.name, connected_ap, sta.wintfs[0].ip))

                prev_ap[i] = connected_ap

            sleep(2)


def topology(args):
    "Create a network."
    net = Mininet_wifi(controller=Controller)


    n = 20
    stations = []
    for i in range(1, n):
        sta = net.addStation('sta%d' % (i), mac='00:00:00:00:00:%02d' % (i),
                             min_x=100, max_x=2000, min_y=100, max_y=1400, min_v=10, max_v=20)

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

    stations = np.array(stations)

    threading.Thread(target=monitoring, args=(stations,)).start()
    threading.Thread(target=incoming, args=(stations,)).start()

    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
