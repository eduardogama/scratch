import requests

from cachecontrol import CacheControl

# NOTE: This requires lockfile be installed
from cachecontrol.caches import FileCache


HOST = "dash.akamaized.net"  # "localhost"
PORT = 80  # 30001
URL = "http://{}:{}/lifeofpi/dash-avc-aac.mpd".format(HOST, PORT)  # http://localhost:30001/lifeofpi/dash-avc-aac.mpd

URL = f'https://{HOST}/akamai/bbb_30fps/bbb_30fps.mpd'

cache = FileCache('.webcache')
sess = CacheControl(requests.Session(),
                    cache=cache)

# forever_cache = FileCache('.web_cache', forever=True)
#
# sess = CacheControl(requests.Session(), forever_cache)


print(sess)


def main():
    sess = CacheControl(requests.Session(), cache=FileCache('.webcache'))

    response = sess.get(URL)
    print(response.from_cache)
    print(response.content)
    print("=========")

#    cache.delete(URL)

    response = sess.get("https://dash.akamaized.net/dashif/ibc2015/")
    print(response.from_cache)
    print(response.content)

    print(dir(response))
    print(response.raise_for_status)
    print(response.status_code)
    cache.delete(URL)


if __name__ == '__main__':
    main()
