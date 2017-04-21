from datetime import datetime
import sys

from lib import HelperFunctions as hf
from lib import RedisDB as db


def preprocessStrings(fileName):
	"""
	Preprocess strings data.
	:param fileName: the file containing the strings.
	"""
	start = datetime.now()
	with open(fileName, 'r') as file:
		# Read file lines.
		lines = file.readlines()
		data = []
		for line in lines:
			data.append(hf.processStringLine(line))

		# Prepare redis keys for insertion.
		redisKeys = {}
		for i in range(len(data)):
			redisKeys[data[i]['key']] = data[i]['value']

		# Insert keys to redis.
		answer1 = db.buildStringDB(redisKeys)

		redisKeys = {}
		for i in range(len(data)):
			strain = data[i]['key'].split('#')[-1]
			if strain not in redisKeys:
				redisKeys[strain] = []

			redisKeys[strain].append(data[i]['key'])

		answer2 = db.buildStrainsDB(redisKeys)

		# Record time passed.
		timedelta = datetime.now() - start
		if answer1 is True and answer2 is True:
			print('String DB was built successfully from file {} in {}.'.format (fileName, timedelta))


def preprocessTaxa(fileName):
	"""
	Preprocess taxa data.
	:param fileName: the file containing the taxa.
	"""
	start = datetime.now()
	with open(fileName, 'r') as file:
		# Read file lines.
		lines = file.readlines()
		data = []
		for line in lines[1:]:
			data.append(hf.processTaxaLine(line))

		# Prepare redis keys for insertion.
		redisKeys = {}
		for i in range(len(data)):
			for key in data[i]['keys']:
				if key not in redisKeys:
					redisKeys[key] = []

				redisKeys[key].append(data[i]['value'])

		# Insert keys to redis.
		answer = db.buildTaxaDB(redisKeys)

		# Record time passed.
		timedelta = datetime.now() - start
		if answer is True:
			print('Taxa DB was built successfully from file {} in {}.'.format(fileName, timedelta))


def preprocessSigma(fileName):
	"""
	Preprocess sigma data.
	:param fileName: the file containing the sigma data.
	"""
	start = datetime.now()
	with open(fileName, 'r') as file:
		# Read file lines.
		lines = file.readlines()
		data = []
		for line in lines:
			data.append(hf.processSigmaLine(line))

		# Prepare redis keys for insertion.
		redisKeys = {}
		for i in range(len(data)):
			if data[i]['key'] not in redisKeys:
				redisKeys[data[i]['key']] = []

			redisKeys[data[i]['key']].extend(x for x in data[i]['value'] if x not in redisKeys[data[i]['key']])

		# Insert keys to redis.
		answer = db.buildSigmaDB(redisKeys)

		# Record time passed.
		timedelta = datetime.now() - start
		if answer is True:
			print('Sigma DB was built successfully from file {} in {}.'.format(fileName, timedelta))


def preprocessCogs(fileName):
	"""
	Preprocess COGs data
	:param fileName: the file containing the COGs data 
	"""
	start = datetime.now()
	with open(fileName, 'r') as file:
		# Read file lines.
		lines = file.readlines()
		data = []
		for line in lines:
			data.append(hf.processCogLine(line))

		# Prepare redis keys for insertion.
		redisKeys = {}
		for i in range(len(data)):
			for j in range(len(data[i]['keys'])):
				if data[i]['keys'][j] not in redisKeys:
					redisKeys[data[i]['keys'][j]] = []

			redisKeys[data[i]['keys'][j]].append(data[i]['value'])

		# Insert keys to redis.
		answer = db.buildCogsDB(redisKeys)

		# Record time passed.
		timedelta = datetime.now() - start
		if answer is True:
			print('COGs DB was built successfully from file {} in {}.'.format(fileName, timedelta))

options = {
	'-taxa': preprocessTaxa,
	'-sigma': preprocessSigma,
	'-strings': preprocessStrings,
	'-cogs': preprocessCogs
}

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print('Not enough arguments!')

	else:
		args = sys.argv[1:]
		for x in range(0, len(args), 2):
			option = hf.argInOption(args[x], options)
			if option and args[x+1]:
				options[args[x]](args[x + 1])
