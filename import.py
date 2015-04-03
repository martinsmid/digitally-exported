#!/usr/bin/env python
import os
import re
import sys
import urllib
import urlparse
import logging
import json

# export backends
from exaile import Exaile
from rhythmbox import Rhythmbox
from dummy import Dummy

class WindowsOpener(urllib.FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'

re_mount_point = re.compile('(/.*)')

def process(url, backend):
    myopener = WindowsOpener()
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

    logging.info('Exporting.')
    # export to backend
    for href, radio in stations.iteritems():
        backend.add(radio['genre'], radio['uri'])
    backend.finish()

def main():
    logging.basicConfig(level=logging.INFO)
    backend = Rhythmbox()
    if len(sys.argv) == 1:
        url = 'http://listen.di.fm/public2'
        process(url, backend)
    else:
        for url in sys.argv[1:]:
            process(url, backend)

#############################################################################

if __name__ == "__main__":
    main()

