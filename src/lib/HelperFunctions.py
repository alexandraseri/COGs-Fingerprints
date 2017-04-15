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

def getAllTaxa():
	"""
	Return all taxa families from taxaDB.
	:return: an array of all the families.
	"""
	return db.getTaxaDB()