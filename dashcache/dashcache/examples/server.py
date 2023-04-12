from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer

import ssl  # noqa: F401
import requests
import simplejson

from cachecontrol import CacheControl
from cachecontrol.caches import FileCache  # NOTE: This requires lockfile be installed

from lrucache import LRUCache
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


HOSTNAME_SERVER = "0.0.0.0"
HOSTNAME_PORT = 3030
endpoint = f'http://{HOSTNAME_SERVER}:{HOSTNAME_PORT}'

# CLOUD_IP = "http://dash.akamaized.net"
CLOUD_SERVER = "localhost"
CLOUD_PORT = 80
cloud_url = f'https://{CLOUD_SERVER}:{CLOUD_PORT}/akamai/bbb_30fps/bbb_30fps.mpd'

filecache = FileCache('.webcache')
cacheCtrl = LRUCache(10, filecache)
sessCtrl = CacheControl(requests.Session(), cache=filecache)


class RequestHandler(SimpleHTTPRequestHandler):

    def __init__(self):
        self.addr = "localhost:30000"

    def do_GET(self):
        # cloud_url = "http://{}:{}{}".format(CLOUD_SERVER, CLOUD_PORT, self.path)
        cloud_url = f'https://dash.akamaized.net{self.path}'

        response = sessCtrl.get(cloud_url)
        print("Response from cache:", response.from_cache)

        if response.status_code == 200:
            cacheCtrl.filecache_store_request(cloud_url)

        self.send_response(200)
        self.send_header('Location', endpoint)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response.content)

    def proactive_approach(self):
        pass

    def do_POST(self):
        self._set_headers()
        print("in post method")
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        self.send_response(200)
        self.end_headers()

        data = simplejson.loads(self.data_string)
        with open("test123456.json", "w") as outfile:
            simplejson.dump(data, outfile)
        print("{}".format(data))
        f = open("for_presen.py")
        self.wfile.write(f.read())
        return


class Main():
    def run(self):
        address = (HOSTNAME_SERVER, HOSTNAME_PORT)

        vodServer = HTTPServer(address, RequestHandler)
        vodServer.allow_reuse_address = True

        try:
            # Start the server
            print("Server started %s" % (endpoint))
            vodServer.serve_forever()
        except KeyboardInterrupt:
            print("Error Exception")

        vodServer.server_close()

        cacheCtrl.close()
        sessCtrl.close()

        print("Server stopped.")


if __name__ == "__main__":
    main = Main()
    main.run()
