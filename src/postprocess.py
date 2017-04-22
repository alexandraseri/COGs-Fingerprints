import ast
from datetime import datetime
import sys

from lib import HelperFunctions as hf

""" Global variables """
family = ''
fingerprints = {}
strings = []
resultsDirectory = ''


def absoluteThreshold():
	"""
	Calculate fingerprints who appear more than the threshold in family's strings, and write results to file.
	"""
	start = datetime.now()
	strings = hf.getFamilyStrings(family)
	threshold = [0.05, 0.1, 0.2, 0.3, 0.5, 0.8]
	for x in range(len(threshold)):
		thresholdFingerprints = hf.getAboveThreshold(threshold[x], len(strings), fingerprints)

		if len(thresholdFingerprints.keys()) > 0:
			with open(resultsDirectory + family + '_fingerprint_' + str(threshold[x]) + '.txt', 'w+') as file:
				file.write('Total number of strings in family: {}.\n'.format(len(strings)))

				for fingerprint in thresholdFingerprints:
					fpStrings = ', '.join(thresholdFingerprints[fingerprint])
					numOfStrings= len(thresholdFingerprints[fingerprint])
					line = '--- Fingerprint: {} : numOfStrings: {} \n------in strings: {} \n'
					file.write(line.format(fingerprint, numOfStrings, fpStrings))

	# Record time passed.
	print('Threshold calculation runtime: {}.'.format(datetime.now() - start))


def cogsProcess(cogsString):
	"""
	Calculate fingerprints who have COGs with the function list provided, calculate thresholds and write results to file. 
	:param cogsString: the provided function list for COGs
	"""
	if cogsString:
		try:
			cogsList = ast.literal_eval(cogsString)
			cogs = hf.getCogs(cogsList)
			start = datetime.now()
			cogsFingerprints = hf.analyzeCogsFingerprints(cogs, fingerprints)
			numOfStrings = hf.getCountOfStrings(cogsFingerprints)

			print('Checking thresholds for the {} different strings in relevant fingerprints.'.format(len(strings)))
			threshold = [0.05, 0.1, 0.2, 0.3, 0.5, 0.8]

			filename = family + '_with_cogs'
			for cog in cogs:
				for i in range(cogs[cog]['repeat']):
					filename += '_' + cog

			for x in range(len(threshold)):
				thresholdFingerprints = hf.getAboveThreshold(threshold[x], numOfStrings, cogsFingerprints)

				if len(thresholdFingerprints.keys()) > 0:
					with open(resultsDirectory + filename + '_fingerprint_' + str(threshold[x]) + '.txt', 'w+') as file:
						list = ';'.join(cogsList)
						file.write('Total number of strings in family with COGs function [{}] : {}.\n\n'.format(list, numOfStrings))

						for fingerprint in thresholdFingerprints:
							fpStrings = ', '.join(thresholdFingerprints[fingerprint])
							line = '--- Fingerprint: {} : numOfStrings: {}\n------in strings: {} \n'
							file.write(line.format(fingerprint, len(thresholdFingerprints[fingerprint]), fpStrings))

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
		resultsDirectory = sys.argv[1] + '/'
		args = sys.argv[2:]
		family = args[0]
		filepath = resultsDirectory + family + '_fingerprints.txt'
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
