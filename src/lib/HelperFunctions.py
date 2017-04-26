import ast

import Consts
import RedisDB as db


def buildRedisKey(index, name):
	"""
	Build a redis key for each kind of 'family'
	:param index: the type of 'family'. See Consts.redisPrefixWords doc
	:param name: the name of the 'family'
	:return: a string representing the redis key for requested 'family'
	"""
	return (Consts.redisPrefixWords[index] + name).rstrip()


def processTaxaLine(line):
	"""
	Process taxa data line from taxa file.
	:param line: the line from data file to process
	:return: an Object with value as strain_id and keys as all the 'families' associated with it
	"""
	lineArray = line.split(',')
	keys = []
	for i in range(len(lineArray)):
		if i != 6 and i != 5 and lineArray[i] not in  ['-', '-\n', '', ' ']:
			keys.append(buildRedisKey(i, lineArray[i]))

	return {'value': lineArray[6], 'keys': keys}


def processSigmaLine(line):
	"""
	Process sigma line from data file
	:param line: the line from data file to process
	:return: an Object with key as the strain_id and value as the array of COGs within the line
	"""
	lineArray = line.split()
	key = lineArray[0].split('#')[-1]
	return {'key': key, 'value': lineArray[1:]}


def processStringLine(line):
	"""
	Process string line from data file.
	:param line: the line from data file to process
	:return: an Object with key as the name_string and value as the string of COGs within the line, 
	separated by ;
	"""
	lineArray = line.split()
	key = lineArray[0]
	value = ';'.join(lineArray[1:])
	return {'key': key, 'value': value}


def processCogFunctionLine(line):
	"""
	Process COG line for function from data file
	:param line: the line from the data file to process
	:return: an Object with the key as the function of the cog and value as the cog id number
	"""
	lineArray = line.split(';')
	keys = []
	for x in range(len(lineArray[1])):
		keys.append(lineArray[1][x])

	value = lineArray[0][3:]
	return {'keys': keys, 'value': value}


def processCogListLine(line):
	"""
	Process COG line for list from data file
	:param line: the line from the data file to process
	:return: an Object with key as COG id and value as COG function
	"""
	lineArray = line.split(';')
	key = lineArray[0][3:]
	value = lineArray[1]
	return {'key': key, 'value': value}


def getFamilySigma(family):
	"""
	Get the family's sigma.
	:param family: the requested family 
	:return: an array of sigma associated with requested family
	"""
	return db.getTaxaFamilySigma(family)


def getFamilyStrings(family):
	"""
	Get the family's strings
	:param family: the requested family
	:return: an array of string associated with requested family
	"""
	return db.getTaxaFamilyStrings(family)


def createLife(string, sigma):
	"""
	Create a LIFE object for algorithm
	:param string: the LIFE's string
	:param sigma: the sigma
	:return: an Object with keys: 'string' as the LIFE's string, 
	'letters' as an Object containing all the COGs from sigma
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
	Return all taxa with family type from taxaDB
	:param familyType: the family type requested
	:return: an array of all the relevant taxa
	"""
	return db.getTaxaType(familyType)


def argInOption(arg, options):
	"""
	Check if argument is one of the options
	:param arg: the argument given
	:param options: the options to check
	:return: if is an option, return a function, else, returns false
	"""
	if arg not in options:
		print('You have to provide a valid option: {}. You provided {}.'.format(', '.join(options.keys()), arg))
		return False

	return options[arg]


def getFingerprints(file):
	"""
	Get all fingerprints from file
	:param file: the fingerprints file
	:return: an Object with keys as fingerprints and values as the strings
	"""
	lines = file.readlines()
	fingerprints = {}
	fingerprint = ''
	for line in lines:
		if 'fingerprint' in line:
			fingerprint = line.split(': ')[1].rstrip()
		elif 'in strings' in line:
			fingerprints[fingerprint] = line.split(': ')[1].rstrip().split(', ')

	return fingerprints


def getAboveThreshold(threshold, numOfStrings, fingerprints):
	"""
	Get all results above certain threshold number and return them
	:param threshold: the requested % of the strings with the same fingerprint
	:param family: the family
	:param strings: the family's strings
	:param fingerprints: the fingerprints object
	:return an Object with the relevant fingerprints and their strings
	"""
	minNumber = numOfStrings * threshold
	relevantFingerprints = {}
	for fingerprint in fingerprints:
		if len(fingerprints[fingerprint]) > minNumber:
			relevantFingerprints[fingerprint] = fingerprints[fingerprint]

	return relevantFingerprints


def getCogsFunctions(cogsList):
	"""
	Gets cogs list per function provided in cogsList
	:param cogsList: the cog's functions list
	:return: an Object with the key as a cog function, and value as an Object with a repeat key for num of repeats 
	and a key for list of cogs
	"""
	cogsDict = {}
	for x in range(len(cogsList)):
		if cogsList[x] not in cogsDict:
			cogsDict[cogsList[x]] = {
				'repeat': 1,
				'list': []
			}
		else:
			cogsDict[cogsList[x]]['repeat'] += 1

	for cog in cogsDict:
		list = db.getCogsForFunction(cog)
		if list:
			try:
				cogs = ast.literal_eval(list)
			except ValueError:
				print('Can\'t get cogs list for cog function [{}]. There was an error when retrieving cogs list.'.format(cog))
				exit()

			cogsDict[cog]['list'] = cogs

		else:
			print('Can\'t get cogs list for cog function [{}]. There are no cogs for this function.'.format(cog))
			exit()

	return cogsDict


def analyzeCogsFingerprints(cogs, fingerprints):
	"""
	Calculate and analyze all fingerprints with given cogs
	:param cogs: the cogs to search for 
	:param fingerprints: the fingerprints to search
	:return: an Object with keys as relevant fingerprints and values as the strings with those fingerprints 
	"""
	relevantFingerprints = {}

	for fingerprint in fingerprints:
		cogsCounter = {}
		for cog in cogs:
			cogsCounter[cog] = 0

		fpCogs = fingerprint.split(';')
		for cog in cogs:
			for i in range(len(fpCogs)):
				if fpCogs[i] in cogs[cog]['list']:
					cogsCounter[cog] += 1

		all = 0
		for cog in cogs:
			if cogsCounter[cog] >= cogs[cog]['repeat']:
				all += 1

		if all == len(cogs.keys()):
			fingerprintWithFunctions = fingerprint + ' : '
			for i in range(len(fpCogs)):
				fingerprintWithFunctions += db.getCogFunction(fpCogs[i]) + ';'

			relevantFingerprints[fingerprintWithFunctions[:-1]] = fingerprints[fingerprint]

	return relevantFingerprints


def getCountOfStrings(fingerprints):
	"""
	Returns the number of different strings in fingerprints object
	:param fingerprints: the fingerprints object 
	:return: the number of different strings 
	"""
	stringsDict = {}
	for fingerprint in fingerprints:
		strings = fingerprints[fingerprint]
		for i in range(len(strings)):
			if strings[i] not in stringsDict:
				stringsDict[strings[i]] = 0

			stringsDict[strings[i]] += 1

	return len(stringsDict.keys())


def getCogsList(cogsList):
	"""
	Gets cogs list per cog number provided in cogsList
	:param cogsList: the cogs numbers list
	:return: an Object with the key as a cog number, and value as a repeat key 
	"""
	cogsDict = {}
	for x in range(len(cogsList)):
		if cogsList[x] not in cogsDict:
			cogsDict[cogsList[x]] = 1
		else:
			cogsDict[cogsList[x]] += 1

	return cogsDict


def findFingerprintsWithCogs(cogs, fingerprints):
	"""
	Find all fingerprints with given cogs
	:param cogs: the cogs to search for 
	:param fingerprints: the fingerprints to search
	:return: an Object with keys as relevant fingerprints and values as the strings with those fingerprints 
	"""
	relevantFingerprints = {}

	for fingerprint in fingerprints:
		cogsCounter = {}
		for cog in cogs:
			cogsCounter[cog] = 0

		fpCogs = fingerprint.split(';')
		for cog in cogs:
			if cog in fpCogs:
				cogsCounter[cog] += 1

		all = 0
		for cog in cogs:
			if cogsCounter[cog] >= cogs[cog]:
				all += 1

		if all == len(cogs.keys()):
			fingerprintWithFunctions = fingerprint + ' : '
			for i in range(len(fpCogs)):
				fingerprintWithFunctions += db.getCogFunction(fpCogs[i]) + ';'

			relevantFingerprints[fingerprintWithFunctions[:-1]] = fingerprints[fingerprint]

	return relevantFingerprints
