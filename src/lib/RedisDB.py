import redis
import ast

""" Taxa redis client """
taxaClient = redis.StrictRedis(host='localhost', port=6379, db=0)

""" Sigma redis client """
sigmaClient = redis.StrictRedis(host='localhost', port=6379, db=1)

""" Strings redis client """
stringClient = redis.StrictRedis(host='localhost', port=6379, db=2)

""" Strains redis client """
strainClient = redis.StrictRedis(host='localhost', port=6379, db=3)

""" COGs functions redis client """
cogsFunctionClient = redis.StrictRedis(host='localhost', port=6379, db=4)

""" COGs list redis client """
cogsListClient = redis.StrictRedis(host='localhost', port=6379, db=5)


def buildTaxaDB(keys):
	"""
	Construct taxaDB in redis.
	:param keys: the keys to insert to DB with their values.
	:return: True when finished
	"""
	taxaClient.flushdb() 	# Flush existing contents of taxa DB

	pipe = taxaClient.pipeline()
	for key in keys:
		pipe.set(key, keys[key])

	pipe.execute()
	return True


def getTaxaType(familyType):
	"""
	Return all keys of taxaDB with family type
	:param familyType: the family type requested.
	:return: an array of keys from taxaDB.
	"""
	taxa = []
	match = familyType+'_*'
	for key in taxaClient.scan_iter(match=match):
		taxa.append(key)

	return taxa


def buildSigmaDB(keys):
	"""
	Construct sigmaDB in redis.
	:param keys: the keys to insert to DB with their values.
	:return: True when finished
	"""
	sigmaClient.flushdb() # Flush existing contents of sigma DB

	pipe = sigmaClient.pipeline()
	for key in keys:
		pipe.set(key, keys[key])

	pipe.execute()
	return True

def getTaxaFamilySigma(family):
	"""
	Get the sigma associated with the requested family.
	:param family: the requested family.
	:return: an array of sigma as requested.
	"""
	taxaString = taxaClient.get(family)
	answer = []
	if(taxaString):
		strains =  ast.literal_eval(taxaString)
		pipe = sigmaClient.pipeline()
		for strain in range(len(strains)):
			pipe.get(strains[strain])

		get = (pipe.execute())
		for i in range(len(get)):
			if get[i] and len(get[i]) > 0:
				array = ast.literal_eval(get[i])
				answer.extend(array[x] for x in range(len(array)) if array[x] not in answer)

	return answer

def buildStringDB(keys):
	"""
	Construct sigmaDB in redis.
	:param keys: the keys to insert to DB with their values.
	:return: True when finished
	"""

	stringClient.flushdb() # Flush existing contents of strings DB

	pipe = stringClient.pipeline()
	for key in keys:
		pipe.set(key, keys[key])

	pipe.execute()
	return True


def getTaxaFamilyStrings(family):
	"""
	Get the strings associated with the requested family.
	:param family: the requested family.
	:return: an array of strings.
	"""
	taxaString = taxaClient.get(family)
	strings = []
	if taxaString and len(taxaString) > 0:
		strains = ast.literal_eval(taxaString)
		pipe = strainClient.pipeline()
		for strain in range(len(strains)):
			pipe.get(strains[strain])

		get = (pipe.execute())
		for i in range(len(get)):
			if get[i] and len(get[i]) > 0:
				stringsArray = ast.literal_eval(get[i])
				for j in range(len(stringsArray)):
					string = {
						'id': stringsArray[j].split('#')[-1],
						'name': stringsArray[j],
						'string': stringClient.get(stringsArray[j])
					}

					strings.append(string)

	return strings


def buildStrainsDB(keys):
	"""
	Construct strainsDB in redis.
	:param keys: the keys to insert to DB with their values.
	:return: True when finished
	"""
	strainClient.flushdb() # Flush existing contents of strains DB

	pipe = strainClient.pipeline()
	for key in keys:
		pipe.set(key, keys[key])

	pipe.execute()
	return True


def buildCogsFunctionDB(keys):
	"""
	Construct cogsDB in redis
	:param keys: the keys to insert to DB with their values.
	:return: True when finished
	"""
	cogsFunctionClient.flushdb() # Flush existing contents of cogs DB

	pipe = cogsFunctionClient.pipeline()
	for key in keys:
		pipe.set(key, keys[key])

	pipe.execute()
	return True


def getCogsForFunction(function):
	"""
	Get all cogs with the given function
	:param function: the wanted function
	:return: list of cogs with that function
	"""
	cogsList = cogsFunctionClient.get(function)
	return cogsList


def buildCogsListDB(keys):
	"""
	Construct cogsDB in redis
	:param keys: the keys to insert to DB with their values.
	:return: True when finished
	"""
	cogsListClient.flushdb() # Flush existing contents of cogs DB

	pipe = cogsListClient.pipeline()
	for key in keys:
		pipe.set(key, keys[key])

	pipe.execute()
	return True


def getCogFunction(cog):
	"""
	Returns the function for requested cog id
	:param cog: the cog to find
	:return: the function of the cog
	"""
	function = cogsListClient.get(cog)
	if not function:
		return cog

	return function
