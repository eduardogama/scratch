from flask import Flask
from flask import Response
from flask import request
# from flask import redirect
from lrucache import LRUCache

from cachecontrol import CacheControl
from cachecontrol.caches import FileCache  # NOTE: This requires lockfile be installed

import os
import atexit
import pathlib
import requests

from middleware import setup_metrics
from middleware import REQUEST_COUNT, REQUEST_LATENCY
from prometheus_client import generate_latest, Gauge


app = Flask(__name__)
#setup_metrics(app)

CACHE_SIZE = 40


# Create a metric to track time spent and requests made.
#REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
cache_metrics = Gauge(
    'cache_metrics',
    'Cache hit or cache miss (Cache size)',
    ['hit', 'ext']
)
CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

filecache = FileCache('.webcache')
cacheCtrl = LRUCache(CACHE_SIZE, filecache)
sessCtrl = CacheControl(
    requests.Session(), 
    cache=filecache
)


@app.route('/<path:path>')
def get_endpoint(path) -> Response:
    cloud_url = 'http://143.106.73.50:30002/{}'.format(path)

    response = sessCtrl.get(cloud_url)
        
    if response.status_code == 200:
        cacheCtrl.filecache_store_request(cloud_url, len(response.content))
    
        cache_metrics.labels(
            response.from_cache,        # Bollean variable for cache hit
            pathlib.Path(path).suffix   # extract suffix file (ex. mpd, m4v, mp4...)
        ).inc()

    return Response(
        response.content,               # Cache content 
        status=response.status_code,    # status code usually 200
        headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization'
        }
    )


@app.route("/metrics")
def request_metrics() -> Response:
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    

@app.route("/reset")
def reset_metrics() -> Response:

    cache_metrics._metrics.clear()
    
    res = ""
    while not cacheCtrl.filecache_is_empty():
        res += cacheCtrl.filecache_pop() + "\n"
    
    capacity = request.args.get('capacity', default=CACHE_SIZE, type=int) 
    cacheCtrl.filecache_setcapacity(capacity)
    
    res += "Current capacity = " + str(cacheCtrl.filecache_current_size()) + "\n"
    res += "New Capacity = " + str(capacity)
    
    return Response(res, mimetype=CONTENT_TYPE_LATEST)


def OnExitApp() -> None:
    cacheCtrl.close()
    sessCtrl.close()


atexit.register(OnExitApp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
