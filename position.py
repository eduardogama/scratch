#!/usr/bin/env python

'Setting position of the nodes'

import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from mn_wifi.node import UserAP
from mininet.nodelib import NAT


def addNAT(self, name='nat0', connect=True, inNamespace=False,
            linkTo=None, **params):
    """Add a NAT to the Mininet network
        name: name of NAT node
        connect: switch to connect to | True (s1) | None
        inNamespace: create in a network namespace
        params: other NAT node params, notably:
            ip: used as default gateway address"""
    nat = self.addHost(name, cls=NAT, inNamespace=inNamespace,
                        subnet=self.ipBase, **params)
    # find first ap and create link
    if connect:
        if not isinstance(connect, Node):
            if linkTo:
                nodes = self.switches + self.aps + self.apsensors + self.modems
                for node in nodes:
                    if linkTo == node.name:
                        connect = node
            else:
                if self.switches:
                    connect = self.switches[0]
                elif self.aps:
                    connect = self.aps[0]
        
        # Connect the nat to the ap
        self.addLink(nat, connect)

        # Set the default route on stations
        natIP = nat.params['ip'].split('/')[0]
        nodes = self.stations + self.hosts + self.cars + self.sensors + self.modems
        if 'net' in params:
            for node in nodes:
                if node.inNamespace:
                    self.setStaticRoute(node, '{} via {}'.format(params['net'], natIP))
        else:
            for node in nodes:
                if node.inNamespace:
                    if isinstance(node, self.sensor) or isinstance(node, self.apsensor):
                        node.setDefault6Route('via {}'.format(natIP))
                    else:
                        node.setDefaultRoute('via {}'.format(natIP))
    return nat

def topology(args):

    net = Mininet_wifi()

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:02',
                   position='400,1100,0')
    net.addStation('sta2', mac='00:00:00:00:00:03',
                   position='400,460,0')

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
    

    
    info("*** Configuring propagation model\n")
    net.setPropagationModel(model="logDistance", sL=3, exp=3)

    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Creating links\n")
    # net.addLink(s1, e1)
    net.addLink(e1, e4)
    
    net.addLink(e1, e2)
    net.addLink(e2, e3)
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
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
