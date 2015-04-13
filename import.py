import os
import sys
import logging
from optparse import OptionParser, Option

import targets

parser = OptionParser()
parser.add_option("-s", "--source", dest="sources", default='digitally_imported',
	action="append", help="radio station sources.")
parser.add_option("-t", "--target", dest="targets",
	action="append", help="where to import stations.")
parser.add_option("-q", "--quiet",
	action="store_false", dest="verbose", default=True,
	help="don't print status messages to stdout")


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	(options, args) = parser.parse_args()

	print options
	logging.info('Exporting.')

	# import radio stations
	from sources import digitally_imported
	stations = digitally_imported.get_stations()

	# for every target
	for target in options.targets:
		# import backend
		target_module = getattr(targets, target)
		export_object = target_module.Export()

		# iterate stations
		for key, radio in stations.iteritems():
			export_object.add(radio['genre'], radio['uri'])
		export_object.finish()
