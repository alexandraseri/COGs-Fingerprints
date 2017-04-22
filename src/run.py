from datetime import datetime
import os
import sys

from lib import HelperFunctions as hf
from lib.algorithm import Algorithm


def runAlgorithm(family):
	"""
	Run algorithm for family.
	:param family: the requested family.
	"""
	start = datetime.now()

	# Get sigma
	sigma = hf.getFamilySigma(family)
	print('Sigma size is: {}.'.format(len(sigma)))

	# Get strings
	strings = hf.getFamilyStrings(family)
	print('Total number of strings is: {}.\nGot info for running algorithm in {}.'.format(len(strings), datetime.now() - start))

	start = datetime.now()

	# Run algorithm
	algorithm = Algorithm(sigma, strings, family)
	algorithm.run()
	algorithm.print_fingerprints(sys.argv[1] + '/')

	# Record time passed.
	print('Algorithm runtime: {}.'.format(datetime.now() - start))


def runForType(familyType):
	"""
	Run algorithm for family type.
	:param familyType: the family type requested.
	"""
	start = datetime.now()
	taxa = hf.getAllTaxaType(familyType)
	for x in range(len(taxa)):
		print('--- Running for {}. ---'.format(taxa[x]))
		runAlgorithm(taxa[x])

	# Record time passed.
	print('*** Total runtime for family type {} was  {} ***'.format(familyType, datetime.now() - start))


options = {
	'-f': runAlgorithm,
	'-t': runForType
}

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print('Not enough arguments!')

	else:
		try:
			os.mkdir(sys.argv[1])
			print('{} directory created'.format(sys.argv[1]))

		except WindowsError:
			print('{} directory already exists'.format(sys.argv[1]))

		args = sys.argv[2:]
		option = hf.argInOption(args[0], options)
		if option and args[1]:
			options[args[0]](args[1])
