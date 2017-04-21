import ast
from datetime import datetime
import sys

from lib import HelperFunctions as hf

""" Global variables """
family = ''
fingerprints = {}
strings = []


def absoluteThreshold():
	"""
	Calculate fingerprints who appear more than the threshold in family's strings.
	"""
	start = datetime.now()
	strings = hf.getFamilyStrings(family)
	threshold = [0.05, 0.1, 0.2, 0.3, 0.5, 0.8]
	for x in range(len(threshold)):
		hf.getAboveThreshold(threshold[x], family, strings, fingerprints)

	# Record time passed.
	print('Threshold calculation runtime: {}.'.format(datetime.now() - start))


def cogsProcess(cogsString):
	if cogsString:
		try:
			cogsList = ast.literal_eval(cogsString)
			cogs = hf.getCogs(cogsList)
			start = datetime.now()
			cogsFingerprints = hf.analyzeCogsFingerprints(cogs, fingerprints)
			strings = hf.getCountOfStrings(cogsFingerprints)
			print('Checking thresholds for the {} different strings in relevant fingerprints.'.format(len(strings)))
			threshold = [0.05, 0.1, 0.2, 0.3, 0.5, 0.8]
			for x in range(len(threshold)):
				filename = family + '_with_cogs'
				for cog in cogs:
					for i in range(cogs[cog]['repeat']):
						filename += '_' + cog
				hf.getAboveThreshold(threshold[x], filename, strings, cogsFingerprints)

			print('Cogs calculation runtime: {}.'.format(datetime.now() - start))

		except ValueError:
			print('You have to provide a valid cogs list in the form ["S","V","V"]. You provided {}.'.format(cogsString))
			exit()


options = {
	'-threshold': absoluteThreshold,
	'-cogs': cogsProcess
}

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print('Not enough arguments!')

	else:
		args = sys.argv[1:]
		family = args[0]
		filepath = '../results/' + family + '_fingerprints.txt'
		with open(filepath, 'r+') as file:
			# Read fingerprint file
			print('Getting fingerprints for family {}.'.format(family))
			fingerprints = hf.getFingerprints(file)

			# Read options
			x = 1
			while x < len(args):
				option = hf.argInOption(args[x], options)
				if option:
					print('Starting {} post process option.'.format(args[x]))
					if args[x] == '-cogs' and args[x+1]:
						options[args[x]](args[x+1])
						x += 2
					else:
						options[args[x]]()
						x += 1
