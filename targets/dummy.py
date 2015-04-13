import logging

class Dummy(object):
    def __init__(self):
        logging.debug('Using Dummy printing backend')

    def add(self, name, uri):
        logging.info('Adding %s [%s]' % (name, uri))

    def finish(self):
        pass

class Export(Dummy):
	pass
