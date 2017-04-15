import sys

from lib import HelperFunctions as hf

""" Global variables """
family = ''
fingerprints = []
strings = []


def absoluteThreshold():
	"""
	Calculate fingerprints who appear more than the threshold in family's strings.
	"""
	threshold = [0.05, 0.1, 0.2, 0.3, 0.5, 0.8]
	for x in range(len(threshold)):
		hf.getAboveThreshold(threshold[x], family, strings, fingerprints)

options = {
	'-threshold': absoluteThreshold
}

if __name__ == "__main__":
	# Global variables
	global fingerprints
	global family
	global strings

	if len(sys.argv) < 3:
		print('Not enough arguments!')

	else:
		args = sys.argv[1:]
		filepath = 'results/' + args[0] + 'fingerprints.txt'
		with open(filepath, 'r+') as file:
			family = args[0]
			strings = hf.getFamilyStrings(family)
			# Read fingerprint file
			fingerprints = hf.getFingerprints(file)

			# Read options
			for x in range(1, len(args)):
				option = hf.argInOption(args[x], options)
				if option and args[x+1]:
					options[args[x]]()
