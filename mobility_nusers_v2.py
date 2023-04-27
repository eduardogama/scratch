#!/usr/bin/env python

'Setting the position of nodes and providing mobility'

import sys
import random

import numpy as np


from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi


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

        self.movingDirection = [f"{coord[0]}, {coord[1]}, 0"]

    def addMovement(self, x, y):
        self.movingDirection.append(f"{x}, {y}, 0")

    def addAP(self, ap):
        self.cur_ap.append(ap)


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
        net.addStation('sta%d' % (i), mac='00:00:00:00:00:%02d' % (i),speed=10)

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

    for user, sta in zip(users, net.stations):
        sta.coord = user.movingDirection

    net.startMobility(time=0)

    for user, sta in zip(users, net.stations):
        net.mobility(sta, 'start', time=1, position=user.movingDirection[0])
        net.mobility(sta, 'stop', time=100, position=user.movingDirection[-1])
    net.stopMobility(time=101)

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
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
