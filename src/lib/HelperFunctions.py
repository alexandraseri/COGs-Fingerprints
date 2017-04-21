import Consts
import RedisDB as db


def buildRedisKey(index, name):
	"""
	Build a redis key for each kind of 'family'
	:param index: the type of 'family'. See Consts.redisPrefixWords doc.
	:param name: the name of the 'family'.
	:return: a string representing the redis key for requested 'family'.
	"""
	return (Consts.redisPrefixWords[index] + name).rstrip()


def processTaxaLine(line):
	"""
	Process taxa data line from taxa file. 
	:param line: the line from data file to process.
	:return: an Object with value as strain_id and keys as all the 'families' associated with it.
	"""
	lineArray = line.split(',')
	keys = []
	for i in range(len(lineArray)):
		if i != 6 and i != 5 and lineArray[i] not in  ['-', '-\n', '', ' ']:
			keys.append(buildRedisKey(i, lineArray[i]))

	return {'value': lineArray[6], 'keys': keys}


def processSigmaLine(line):
	"""
	Process sigma line from data file.
	:param line: the line from data file to process.
	:return: an Object with key as the strain_id and value as the array of COGs within the line.
	"""
	lineArray = line.split()
	key = lineArray[0].split('#')[-1]
	return {'key': key, 'value': lineArray[1:]}


def processStringLine(line):
	"""
	Process string line from data file.
	:param line: the line from data file to process.
	:return: an Object with key as the name_string and value as the string of COGs within the line, 
	separated by ;.
	"""
	lineArray = line.split()
	key = lineArray[0]
	value = ';'.join(lineArray[1:])
	return {'key': key, 'value': value}


def processCogLine(line):
	"""
	Process COG line from data file
	:param line: the line from the data file to process.
	:return: an Object with the key as the function of the cog and value as the cog id number
	"""
	lineArray = line.split(';')
	keys = []
	for x in range(len(lineArray[1])):
		keys.append(lineArray[1][x])

	value = lineArray[0][3:]
	return {'keys': keys, 'value': value}


def getFamilySigma(family):
	"""
	Get the family's sigma. 
	:param family: the requested family .
	:return: an array of sigma associated with requested family.
	"""
	return db.getTaxaFamilySigma(family)


def getFamilyStrings(family):
	"""
	Get the family's strings.
	:param family: the requested family.
	:return: an array of string associated with requested family.
	"""
	return db.getTaxaFamilyStrings(family)


def createLife(string, sigma):
	"""
	Create a LIFE object for algorithm.
	:param string: the LIFE's string.
	:param sigma: the sigma.
	:return: an Object with keys: 'string' as the LIFE's string, 
	'letters' as an Object containing all the COGs from sigma.
	"""
	life = {
		'string': string,
		'letters': {}
	}
	for i in range(len(sigma)):
		life['letters'][sigma[i]] = 0

	return life


def getAllTaxaType(familyType):
	"""
	Return all taxa families from taxaDB.
	:param familyType: the family type requested.
	:return: an array of all the families.
	"""
	return db.getTaxaType(familyType)


def argInOption(arg, options):
	"""
	Check if argument is one of the options.
	:param arg: the argument given.
	:param options: the options to check.
	:return: if is an option, return a function, else, returns false.
	"""
	if arg not in options:
		print('You have to provide a valid option: {}. You provided {}.'.format(', '.join(options.keys()), arg))
		return False

	return options[arg]


def getFingerprints(file):
	"""
	Get all fingerprints from file
	:param file: the fingerprints file.
	:return: an Object with keys as fingerprints and values as the strings.
	"""
	lines = file.readlines()
	fingerprints = {}
	fingerprint = ''
	for line in lines:
		if 'fingerprint' in line:
			fingerprint = line.split(': ')[1].rstrip()
		elif 'strings' in line:
			fingerprints[fingerprint] = line.split(': ')[1].rstrip().split(', ')

	return fingerprints


def getAboveThreshold(threshold, family, strings, fingerprints):
	"""
	Get all results above certain threshold number and write them to files in results folder.
	:param threshold: the requested % of the strings with the same fingerprint.
	:param family: the family.
	:param strings: the family's strings.
	:param fingerprints: the fingerprints object
	"""
	minNumber = len(strings) * threshold
	with open('../results/' + family + '_fingerprint_' + str(threshold) + '.txt', 'w+') as file:
		for key in fingerprints.keys():
			if len(fingerprints[key]) > minNumber:
				file.write('--- Fingerprint: {} \n------in strings: {} \n'.format(key, ', '.join(fingerprints[key])))

