import os
import re
import sys
import urllib
import urlparse
import logging
import json

class WindowsLikeOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'

re_mount_point = re.compile('(/.*)')

def get_stations():
    url = 'http://listen.di.fm/public2'

    myopener = WindowsLikeOpener()
    page = myopener.open(url)

    logging.info('Loading page.')
    text = page.read()
    page.close()

    logging.info('Parsing.')
    radio_list = json.loads(text)

    logging.info('Processing stations.')
    stations = {}

    hrefs = {}
    for station in radio_list:
        if station['key'] in hrefs.keys():
            logging.debug('Skipping %s' % station['uri'])
            continue

        stations[station['key']] = {
            'genre': station['name'],
            'key': station['key'],
            'uri': station['playlist'],
        }

    return stations
