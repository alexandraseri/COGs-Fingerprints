import redis


taxaClient = redis.StrictRedis(host='localhost', port=6379, db=0)
sigmaClient = redis.StrictRedis(host='localhost', port=6379, db=1)

def buildTaxaDB(keys):
	# Flush current contents of taxa DB
	taxaClient.flushdb()

	#insert new taxa DB
	pipe = taxaClient.pipeline()
	for key in keys:
		pipe.set(key, keys[key])

	pipe.execute()
	return True

def buildSigmaDB(keys):
	# Flush current contents of sigma DB
	sigmaClient.flushdb()

	#insert new sigma DB
	pipe = sigmaClient.pipeline()
	for key in keys:
		pipe.set(key, keys[key])

	pipe.execute()
	return True