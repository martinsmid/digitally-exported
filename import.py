#!/usr/bin/env python
import os
import re
import sys
import urllib
import urlparse
import logging
from BeautifulSoup import BeautifulSoup

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
    soup = BeautifulSoup(text)

    hrefs = {}

    # for tag in soup.findAll('a', href=True):
    for stream in soup.findAll('div', 'roundcont'):
        # url here: /html/body/div[1]/div[281]/div[2]/div/table/tbody/tr/td[1]/h3
        genre = stream.findAll('tr')[7].findAll('td')[1].text
        tag = stream.findAll('a', href=True)[1]
        parsed = urlparse.urlparse(tag['href'], scheme='http')
        href = parsed.geturl()
        mount_point_text = stream.find('h3').text
        mount_point = re_mount_point.search(mount_point_text).groups()[0]
        uri = urlparse.urljoin(url, mount_point)

        if href.endswith('.xsl') or href.endswith('di.fm'):
            continue

        if uri in hrefs.keys():
            continue

        hrefs[href] = {
            'genre': genre,
            'href': href,
            'uri': uri
        }

    # export to backend
    for href, radio in hrefs.iteritems():
        backend.add(radio['genre'], radio['uri'])
    backend.finish()

def main():
    logging.basicConfig(level=logging.INFO)
    backend = Rhythmbox()
    if len(sys.argv) == 1:
        url = 'http://pub7.di.fm'
        process(url, backend)
    else:
        for url in sys.argv[1:]:
            process(url, backend)

#############################################################################

if __name__ == "__main__":
    main()

