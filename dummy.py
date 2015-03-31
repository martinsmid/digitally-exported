import logging

class Dummy(object):
    def __init__(self):
        print 'Using Dummy'

    def add(self, name, uri):
        logging.info('Adding %s [%s]' % (name, uri))

    def finish(self):
        logging.info('---')
