#!/usr/bin/env python

'Setting the position of nodes and providing mobility'

import os
import sys
import json
import math
import random

import numpy as np
from time import sleep
from threading import Thread

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mininet.node import Controller
from mn_wifi.net import Mininet_wifi
from mininet.term import makeTerm


graph = [
    [1, 3],
    [0, 2, 4],
    [1, 5],
    [0, 4],
    [1, 3, 5],
    [2, 4]
]

aps_pos = [
    [400, 1050, 0],
    [1000, 1050, 0],
    [1600, 1050, 0],
    [400, 450, 0],
    [1000, 450, 0],
    [1600, 450, 0],
]


class User(object):
    def __init__(self, name, ap, coord) -> None:
        self.name = name
        self.ap = ap

        self.cur_ap = [0]
        self.pos_x = coord[0]
        self.pos_y = coord[1]

        self.movingDirection = [f'{coord[0]},{coord[1]},0']
        self.iteratorMovement = None

    def addMovement(self, x, y):
        self.movingDirection.append(f'{x},{y},0')

    def addAP(self, ap):
        self.cur_ap.append(ap)

    def setIterator(self):
        self.iteratorMovement = iter(self.movingDirection[1:])


def positioning(stas, users, niter):

    sleep(10)
    for i in range(niter):
        for sta, user in zip(stas, users):
            pos = next(user.iteratorMovement)
            sta.setPosition(pos)
        sleep(10)


def nextTime(rateParameter, RAND_MAX=0):
    return -math.log(1.0 - random.random()/(RAND_MAX + 1)) / rateParameter


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
            'http://100.112.108.237:3000/samples/ericsson/vod-client.html?userid={}'.format(sta.name))


def topology(args):

    niter = 10
    nusers = 1
    users = []
    coords = {"sta%d" % i: (0, []) for i in range(1, nusers+1)}

    # Starting point forn Access Point 1
    for i, c in enumerate(coords):
        coord = [random.randint(aps_pos[0][0]-150, aps_pos[0][0]+150),
                 random.randint(aps_pos[0][1]-150, aps_pos[0][1]+150), 0]

        user = User(
            name="sta%d" % i,
            ap=0,
            coord=coord
        )

        users.append(user)

    for i in range(10):
        for u in users:
            next_hop = random.choice(graph[u.cur_ap[-1]])
            x = random.randint(
                aps_pos[next_hop][0]-150, aps_pos[next_hop][0]+150)
            y = random.randint(
                aps_pos[next_hop][1]-150, aps_pos[next_hop][1]+150)

            u.addAP(next_hop)
            u.addMovement(x, y)

    for u in users:
        u.setIterator()

    "Create a network."
    net = Mininet_wifi(controller=Controller)

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

    for i in range(1, nusers+1):
        net.addStation('sta%d' % (i), mac='00:00:00:00:00:%02d' %
                       (i), position=users[i-1].movingDirection[0])

    info("*** Configuring propagation model\n")
    net.setPropagationModel(model="logDistance", exp=3)

    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Associating and Creating links\n")
    net.addLink(e1, e2)
    net.addLink(e2, e3)
    net.addLink(e3, e4)
    net.addLink(e4, e5)
    net.addLink(e5, e6)

    if '-p' not in args:
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

    info("*** Running CLI\n")

    Thread(target=positioning, args=(net.stations, users, niter)).start()
    Thread(target=monitoring, args=(net.stations,)).start()
    Thread(target=incoming, args=(net.stations,)).start()

    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
