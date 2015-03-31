import getpass
from xml.etree.ElementTree import ElementTree, fromstring
import logging

template = """
  <entry type="iradio">
    <title>{title}</title>
    <genre>{genre}</genre>
    <artist></artist>
    <album></album>
    <location>{uri}</location>
    <play-count>0</play-count>
    <last-played></last-played>
    <bitrate></bitrate>
    <date>0</date>
    <media-type>application/octet-stream</media-type>
  </entry>

"""

def get_xml(name, uri):
    return template.format(title=name, genre=name, uri=uri)

def get_entry(title, uri, genre):
    return fromstring(get_xml(title, uri))

class Rhythmbox(object):
    def __init__(self):
        self.path = '/home/%s/.local/share/rhythmbox/rhythmdb.xml' % getpass.getuser()
        self.tree = ElementTree()
        self.tree.parse(self.path)
        self.root = self.tree.getroot()

    def add(self, name, uri, genre=None):
        logging.info('Adding %s [%s]' % (name, uri))
        self.root.append(get_entry(name, uri, genre))

    def finish(self):
        logging.info('Saving file')
        self.tree.write(self.path, xml_declaration=True)
