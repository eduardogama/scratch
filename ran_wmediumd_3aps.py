#!/usr/bin/python

import threading

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.node import OVSKernelAP
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

from model.MobileDevice import MobileDevice

from time import sleep

import numpy as np


class Simulation():

    def __init__(self, nusers) -> None:
        self.net = Mininet_wifi(controller=Controller, link=wmediumd,
                                wmediumd_mode=interference, allAutoAssociation=False)

        info("*** Creating nodes\n")
        self.users = self.createStations(nusers)
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
        sta1 = self.net.addStation('sta1', mac='00:00:00:00:00:10', #ip='10.0.0.1/8',
                                   position='30,30,0')
        sta2 = self.net.addStation('sta2', mac='00:00:00:00:00:20', #ip='10.0.0.2/8',
                                   position='30,40,0')

        user1 = MobileDevice(
            net=self.net,
            name="sta1",
            station=sta1
        )

        user2 = MobileDevice(
            net=self.net,
            name="sta2",
            station=sta2
        )

        return np.array([user1, user2])

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


        info("*** Running CLI\n")
        CLI(self.net)

        info("*** Stopping network\n")
        self.net.stop()


if __name__ == '__main__':
    setLogLevel('info')

    nusers = 10

    sim = Simulation(nusers)
    sim.run()
