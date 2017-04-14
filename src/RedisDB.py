import redis
import ast


taxaClient = redis.StrictRedis(host='localhost', port=6379, db=0)
sigmaClient = redis.StrictRedis(host='localhost', port=6379, db=1)
stringClient = redis.StrictRedis(host='localhost', port=6379, db=2)

def buildTaxaDB(keys):
	# Flush current contents of taxa DB
	taxaClient.flushdb()

	#insert new taxa DB
	pipe = taxaClient.pipeline()
	for key in keys:
		pipe.set(key, keys[key])

	pipe.execute()
	return True


def getTaxaDB():
	taxa = []
	for key in taxaClient.scan_iter():
		taxa.append(key)

	return taxa

def buildSigmaDB(keys):
	# Flush current contents of sigma DB
	sigmaClient.flushdb()

	#insert new sigma DB
	pipe = sigmaClient.pipeline()
	for key in keys:
		pipe.set(key, keys[key])

	pipe.execute()
	return True

def getTaxaFamilySigma(family):
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
	# Flush current contents of strings DB
	stringClient.flushdb()

	#insert new string DB
	pipe = stringClient.pipeline()
	for key in keys:
		pipe.set(key, keys[key])

	pipe.execute()
	return True

def getTaxaFamilyStrings(family):
	taxaString = taxaClient.get(family)
	strings = []
	if(taxaString):
		strains =  ast.literal_eval(taxaString)
		for strain in range(len(strains)):
			match = '*#' + strains[strain]
			for key in stringClient.scan_iter(match=match):
				string = {
					'id': strains[strain],
					'name': key,
					'string': stringClient.get(key)
				}
				strings.append(string)

	return strings