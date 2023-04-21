#!/usr/bin/python


import threading

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.node import OVSKernelAP
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

from time import sleep

import numpy as np


class Simulation():

    def __init__(self, nusers) -> None:
        self.net = Mininet_wifi(controller=Controller, link=wmediumd,
                                wmediumd_mode=interference, allAutoAssociation = False)

        info("*** Creating nodes\n")
        self.stations = self.createStations(nusers)
        self.aps = self.createAccessPoints()

    def run(self) -> None:
        self.topology()

    def createAccessPoints(self) -> object:
        kwargs = {'mode': 'g', 'failMode': 'standalone'}

        self.net.addAccessPoint('ap1', mac='00:00:00:11:00:01',
                                ssid='ap1', channel='1', position='15,30,0', **kwargs)
        self.net.addAccessPoint('ap2', mac='00:00:00:11:00:02',
                                ssid='ap2', channel='6', position='35,30,0', **kwargs)
        self.net.addAccessPoint('ap3', mac='00:00:00:11:00:03',
                                ssid='ap3', channel='11', position='55,30,0', **kwargs)

    def createStations(self, nusers) -> object:
        self.net.addStation('sta1', mac='00:00:00:00:00:10',
                            position='30,30,0')
        self.net.addStation('sta2', mac='00:00:00:00:00:20',
                            position='30,40,0')

        return np.array(self.net.stations)

    def find_ap(self, sta) -> None:
        for ap in self.net.aps:
            sta.wintfs[0].get_rssi(ap.wintfs[0], sta.get_distance_to(ap))

    def topology(self) -> None:

        info("*** Configuring Propagation Model\n")
        self.net.setPropagationModel(model="logDistance", exp=5)

        info("*** Configuring wifi nodes\n")
        self.net.configureWifiNodes()

        self.net.plotGraph(max_x=100, max_y=100)

        info("*** Starting network\n")
        self.net.build()
        self.net.addNAT().configDefault()

        for ap in self.net.aps:
            ap.start([])

        nodes = np.array(self.net.stations)
        # threading.Thread(target=monitoring, args=(nodes,)).start()

        info("*** Running CLI\n")
        CLI(self.net)

        info("*** Stopping network\n")
        self.net.stop()

    def HandoverMgmt(self) -> None:
        while True:
            for sta in self.stations:
                rssi_cmd = "iw dev {}-wlan0 link | grep signal | tr -d signal: | awk '{{print $1 $3}}'".format(
                    sta.name)

                rssi = sta.cmd(rssi_cmd)

                try:
                    # converting to integer
                    rssi = int(rssi)
                except ValueError:
                    rssi = 0

                connected_ap = sta.wintfs[0].ssid
        raise NotImplementedError


def monitoring(stas):
    # Monitor the connectivity of the station
    prev_ap = []
    while True:
        for sta in stas:

            print('Node:', sta.name)
            print('Connected to:', connected_ap)
            print('RSSI:', rssi)

            # Check if the station connects to a different access point
            if connected_ap != prev_ap:
                print('[', sta.wintfs[0].ip, '] Access point changed from',
                      prev_ap, 'to', connected_ap, '! ')
                prev_ap = connected_ap

            # Wait for a few seconds before checking the connectivity again

        sleep(2)


if __name__ == '__main__':
    setLogLevel('info')

    nusers = 10

    sim = Simulation(nusers)
    sim.run()
