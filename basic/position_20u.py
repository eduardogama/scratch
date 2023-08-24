#!/usr/bin/env python

"""Setting the position of nodes and providing mobility"""
from pyvirtualdisplay import Display

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



display = Display()
display.start()


def next_time(rateParameter: float, RAND_MAX: int = 0):
    return -math.log(1.0 - random.random() / (RAND_MAX + 1)) / rateParameter


def SeleniumPlayer(stas: object, abr: str, count: str):
    sleep(2)
    for sta in stas:
        val = next_time(1 / 5.0)
        sleep(val)
        print(sta.wintfs[0].ip, "starting video ... ", sta.wintfs[0].ssid)
        
        makeTerm(sta, cmd='python run-player-main.py {} {} {}'.format(abr, sta.name, count))


def incoming(stas: object, abr: str, count: str):
    SeleniumPlayer(stas, abr, count)


def monitoring(stas):
    # Monitor the connectivity of the station
    prev_ap = np.array([None for i in enumerate(stas)])

    
    for k in range(370):
        for i, sta in enumerate(stas):
            connected_ap = sta.wintfs[0].ssid

            if connected_ap != prev_ap[i]:
                print(
                    json.dumps({
                        "userName": sta.name, 
                        "bsName": connected_ap,
                        "ip": sta.wintfs[0].ip
                    })
                )

                os.system(
                    "curl -X POST 143.106.73.50:30700/collect/handover -H 'Content-Type: application/json' -d $(jo "
                    "userName={} bsName={} ip={})"
                    .format(sta.name, connected_ap, sta.wintfs[0].ip))

                prev_ap[i] = connected_ap
            
        print(2*k, end=' ', flush=True)
        sleep(2)



        def topology(args):

    """Create a network."""
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    abrstr = "abrDynamic"
    nusers = 20

    pos1 = '401.0,1050.0,0.0'
    pos2 = '1001.0,1050.0,0.0'
    pos3 = '1601.0,1050.0,0.0'
    pos4 = '2201.0,1050.0,0.0'

    count = sys.argv[5] if len(sys.argv) > 3 else '0'

    
    for i in range(1, 6):
        net.addStation('sta%d' % i, mac='00:00:00:00:00:%02d' % i, position=pos1)

    for i in range(6, 11):
        net.addStation('sta%d' % i, mac='00:00:00:00:00:%02d' % i, position=pos2)

    for i in range(11, 16):
        net.addStation('sta%d' % i, mac='00:00:00:00:00:%02d' % i, position=pos3)

    for i in range(16, 21):
        net.addStation('sta%d' % i, mac='00:00:00:00:00:%02d' % i, position=pos4)

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

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", sL=3, exp=2.8)

    info("*** Configuring nodes\n")
    net.configureWifiNodes()

    net.addLink(e1, e2)
    net.addLink(e2, e3)
    net.addLink(e3, e4)
    
    info("*** Starting network\n")
    net.build()
    net.addNAT().configDefault()

    e1.start([])
    e2.start([])
    e3.start([])
    e4.start([])


    stations = np.array(net.stations)
    threading.Thread(target=incoming, args=(stations, abrstr, count)).start()

    monitoring(stations)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)


display.stop()
