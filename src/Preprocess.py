from datetime import datetime

from lib import HelperFunctions as hf
from lib import RedisDB as db


def preprocessStrings(fileName):
	"""
	Preprocess strings data.
	:param fileName: the file containing the strings.
	"""
	start = datetime.now()
	with open(fileName, 'r') as file:
		lines = file.readlines()
		data = []
		for line in lines:
			data.append(hf.processStringLine(line))

		redisKeys = {}
		for i in range(len(data)):
			redisKeys[data[i]['key']] = data[i]['value']

		answer = db.buildStringDB(redisKeys)
		timedelta = datetime.now() - start
		if answer is True:
			print('String DB was built successfully from file {} in {}.'.format (fileName[0], timedelta))


def preprocessTaxa(fileName):
	"""
	Preprocess taxa data.
	:param fileName: the file containing the taxa.
	"""
	start = datetime.now()
	with open(fileName[0], 'r') as file:
		lines = file.readlines()
		data = []
		for line in lines[1:]:
			data.append(hf.processTaxaLine(line))

		redisKeys = {}
		for i in range(len(data)):
			for key in data[i]['keys']:
				if key not in redisKeys:
					redisKeys[key] = []

				redisKeys[key].append(data[i]['value'])

		answer = db.buildTaxaDB(redisKeys)
		timedelta = datetime.now() - start
		if answer is True:
			print('Taxa DB was built successfully from file {} in {}.'.format(fileName[0], timedelta))

def preprocessSigma(fileName):
	"""
	Preprocess sigma data.
	:param fileName: the file containing the sigma data.
	"""
	start = datetime.now()
	with open(fileName[0], 'r') as file:
		lines = file.readlines()
		data = []
		for line in lines:
			data.append(hf.processSigmaLine(line))

		redisKeys = {}
		for i in range(len(data)):
			if data[i]['key'] not in redisKeys:
				redisKeys[data[i]['key']] = []

			redisKeys[data[i]['key']].extend(x for x in data[i]['value'] if x not in redisKeys[data[i]['key']])

		answer = db.buildSigmaDB(redisKeys)
		timedelta = datetime.now() - start
		if answer is True:
			print('Sigma DB was built successfully from file {} in {}.'.format(fileName[0], timedelta))
			preprocessStrings(fileName[0])
