import math
import json
import subprocess

from time import sleep
from threading import Thread


class MobileDevice(Thread):
    def __init__(self, net, bgscan_threshold=-76, s_inverval=2, l_interval=5, **kwargs):
        self.environment = net
        self.iuser = kwargs.get('name', 'anonymous')
        self.sta = kwargs.get('station', None)
        self.ap = kwargs.get('ap', None)
        self.controller = kwargs.get(
            'controller_service',
            'http://143.106.73.50:30700/collect/handover'
        )

        self.bgscan_threshold = bgscan_threshold
        self.s_inverval = s_inverval
        self.l_interval = l_interval

        self.f = open(
            '{}.csv'.format(self.iuser), 'a'
        )
        self.f.write('time datarate rssi bts\n')

        Thread.__init__(self)

    def run(self):
        
        self.sta.cmd("wpa_cli -i {}".format(self.sta.params['wlan'][0]))
        
        while True:
            if not self.sta.wintfs[0].ssid:
                self.find_ap()

                sleep(self.l_interval)
            else:
                # rssi_cmd = "iw dev {}-wlan0 link | grep signal | tr -d signal: | awk '{{print $1 $3}}'".format(self.sta.name)
                # rssi = self.sta.cmd(rssi_cmd)
                # rssi = int(rssi) if rssi else -math.inf

                rssi = self.sta.wintfs[0].get_rssi(
                self.ap.wintfs[0], self.sta.get_distance_to(self.ap))

                if rssi <= self.bgscan_threshold:
                    self.find_ap()

                    sleep(self.s_inverval)
                else:
                    sleep(self.l_interval)

    def find_ap(self):

        maxap = None
        maxrssi = -math.inf
        for ap in self.environment.aps:
            rssi = self.sta.wintfs[0].get_rssi(
                ap.wintfs[0], self.sta.get_distance_to(ap))

            if rssi > maxrssi:
                maxap = ap
                maxrssi = rssi

        self.ap = maxap
        self.sta.setAssociation(self.ap, self.sta.wintfs[0].name)

        self.send_msg_controller(self.ap)

    def send_msg_controller(self, ap):
        data = {}
        data['userName'] = self.sta.name
        data['bsName'] = ap.name
        # data['ip'] = ap.server_ip

        json_data = json.dumps(data)

        cmd = [
            'curl', '-X', 'POST', self.controller, '-H',
            'Content-Type: application/json', '-d', json_data
        ]

        try:
            subprocess.check_output(cmd)
        except subprocess.CalledProcessError:
            print(
                "Error sending base station conection from user id {}!".format(
                    self.sta.name
                )
            )

        print(' '.join(cmd))
