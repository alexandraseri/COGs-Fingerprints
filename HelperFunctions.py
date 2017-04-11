import Consts as consts
import RedisDB as db


def buildRedisKey(index, name):
	return consts.redisPrefixWords[index] + name

def analyzeTaxaLine(line):
	lineArray = line.split(',') #Splits into: Kingdom, phylum, class, genus, species, bacteria, strain_id, bacgroup, order
	keys = []
	for i in range(len(lineArray)):
		if i != 6 and i != 5 and lineArray[i] not in  ['-', '-\n', '', ' ']:
			keys.append(buildRedisKey(i, lineArray[i]))

	return {'value': lineArray[6], 'keys': keys}

def analyzeSigmaLine(line):
	lineArray = line.split()
	key = lineArray[0].split('#')[-1]
	return {'key': key, 'value': lineArray[1:]}

def getFamilySigma(family):
	return db.getTaxaFamilySigma(family)

def getFamilyStrings(family):
	pass

def createLife(string, sigma):
	life = {
		'string': string
		'letters': {}
	}
	for i in range(len(sigma)):
		life['letters'][sigma[i]] = 0

	return life