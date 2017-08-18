from datetime import datetime
from pyelasticsearch import ElasticSearch
import sys

from lib import HelperFunctions as hf
from lib.algorithm import Algorithm

es = ElasticSearch()


def runAlgorithm(family):
	"""
	Run algorithm for family.
	:param family: the requested family.
	"""
	start = datetime.now()

	# Get sigma
	sigma = hf.getFamilySigma(family)
	print('Sigma size is: {}.'.format(len(sigma)))

	# Get strings
	strings = hf.getFamilyStrings(family)
	print('Total number of strings is: {}.\nGot info for running algorithm in {}.'.format(len(strings), datetime.now() - start))

	start = datetime.now()

	# Run algorithm
	algorithm = Algorithm(sigma, strings, family)
	algorithm.run()
	algorithm.print_fingerprints(sys.argv[1] + '/')

	# Record time passed.
	print('Algorithm runtime: {}.'.format(datetime.now() - start))


def runForType(familyType):
	"""
	Run algorithm for family type.
	:param familyType: the family type requested.
	"""
	start = datetime.now()
	taxa = hf.getAllTaxaType(familyType)
	for x in range(len(taxa)):
		print('--- Running for {}. ---'.format(taxa[x]))
		runAlgorithm(taxa[x])

	# Record time passed.
	print('*** Total runtime for family type {} was  {} ***'.format(familyType, datetime.now() - start))


def run():
	count = es.count({
		'query': {
			'match_all': {}
		}
	})

	all_string = []
	for i in range(0, count['count'], 10000):
		all_string = sum([all_string, (es.search({
			"query": {
				"match_all": {}
			},
			"size": 10000,
			"from": 0
		}, index='strings', size=10000))['hits']['hits']], [])

	print all_string[0]
	for i in range(len(all_string)):
		words = all_string[i]['_source']['words']
		all_string['']
		for j in range(len(words)):
			set(combinations(all_string[i]['_source']['words'], ))


if __name__ == "__main__":
	run()
