#!/usr/bin/python


from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.node import OVSKernelAP
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mn_wifi.node import UserAP
from model.MobileDevice import MobileDevice
from mininet.term import makeTerm

from time import sleep

import numpy as np


class Simulation():

    def __init__(self) -> None:
        self.net = Mininet_wifi(controller=Controller, link=wmediumd,
                                wmediumd_mode=interference)

        info("*** Creating nodes\n")
        self.ctrl = None
        
        self.users = self.createStations()
        self.aps = self.createAccessPoints()
        
    def run(self) -> None:
        self.topology()

    def createAccessPoints(self) -> object:
        kwargs = {'mode': 'g', 'failMode': 'standalone'}

        ap1 = self.net.addAccessPoint('ap1', mac='00:00:00:11:00:01', passwd='123456789a', encrypt='wpa2',
                                ssid='handover', channel='1', position='15,30,0', **kwargs)
        ap2 = self.net.addAccessPoint('ap2', mac='00:00:00:11:00:02', passwd='123456789a', encrypt='wpa2',
                                ssid='handover', channel='6', position='35,30,0', **kwargs)
        ap3 = self.net.addAccessPoint('ap3', mac='00:00:00:11:00:03', passwd='123456789a', encrypt='wpa2',
                                ssid='handover', channel='11', position='55,30,0', **kwargs)

        self.ctrl = self.net.addController('c1')
        
        return np.array([ap1, ap2, ap3])

    def createStations(self) -> object:
        sta1 = self.net.addStation('sta1', mac='00:00:00:00:00:10', bgscan_threshold=-60,
                                   s_inverval=2, l_interval=5, bgscan_module="simple", position='30,30,0')
        sta2 = self.net.addStation('sta2', mac='00:00:00:00:00:20', bgscan_threshold=-60,
                                   s_inverval=2, l_interval=5, bgscan_module="simple", position='30,40,0')

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

        self.net.addLink(self.aps[0], self.aps[1])
        self.net.addLink(self.aps[1], self.aps[2])

        info("*** Creating links\n")
        self.net.plotGraph(max_x=100, max_y=100)

        info("*** Starting network\n")
        self.net.build()
        self.net.addNAT().configDefault()


        self.ctrl.start()
        for ap in self.net.aps:
            ap.start([self.ctrl])

        for user in self.users:
            user.sta.cmd("wpa_cli -i {} &".format(user.sta.params['wlan'][0]))

        info("*** Running CLI\n")
        CLI(self.net)

        info("*** Stopping network\n")
        self.net.stop()


if __name__ == '__main__':
    setLogLevel('info')

    sim = Simulation()
    sim.run()
