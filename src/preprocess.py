from datetime import datetime
from pyelasticsearch import ElasticSearch
from itertools import combinations

import sys

from lib import HelperFunctions as hf

es = ElasticSearch()


def preprocessStrings(strings, taxa, cogs):
	"""
	Preprocess strings data
	:param strings: the file containing the strings
	:param taxa: the taxa data
	:param cogs: the cogs data
	"""
	start = datetime.now()

	strings_lines = strings.readlines()
	strings_data = []
	for line in strings_lines:
		strings_line = hf.processStringLine(line)

		''' Add taxa data '''
		strings_line['taxa_family'] = taxa[strings_line['strain_id']]

		''' Add COGs data'''
		cogs_list = []
		for i in range(len(strings_line['words'])):
			if strings_line['words'][i] in cogs:
				cogs_list.append(cogs[strings_line['words'][i]])

		strings_line['cogs_info'] = cogs_list

		# ''' Add fingerprints '''
		# words = strings_line['words']
		#
		# fingerprints = []
		# for i in range(1, len(words)):
		# 	comb = set(combinations(words, i))
		# 	list_comb = []
		# 	for c in comb:
		# 		list_comb.append(list(set(c)))
		#
		# 	fingerprints = fingerprints + list_comb
		#
		# strings_line['fingerprints'] = set(tuple(i) for i in fingerprints)

		''' Add to list of strings to insert'''
		strings_data.append(es.index_op(strings_line))

	for i in range(0, len(strings_data), 2000):
		es.bulk(strings_data[i: i+2000], index='strings', doc_type='stringsObject')

	timedelta = datetime.now() - start
	print('Strings data was inserted to db in {}.'.format(timedelta))


def preprocessTaxa(taxa):
	"""
	Preprocess taxa data
	:param taxa: the file containing the taxa
	:return: the taxa data array
	"""
	global taxa_index
	start = datetime.now()
	taxa_lines = taxa.readlines()
	taxa_data = {}
	es_taxa = []
	for line in taxa_lines:
		taxa_line = hf.processTaxaLine(line)
		taxa_data[taxa_line['strain_id']] = taxa_line
		es_taxa.append(es.index_op(taxa_line))

	es.bulk(es_taxa, index='taxa', doc_type='taxaObject')
	timedelta = datetime.now() - start
	print('Taxa data was inserted to db in {}.'.format(timedelta))
	return taxa_data


def preprocessCogs(cogs):
	"""
	Preprocess COGs data
	:param cogs: the file containing the COGs data
	:return: the COGs data array
	"""
	start = datetime.now()
	cogs_lines = cogs.readlines()
	cogs_data = {}
	es_cogs = []
	for line in cogs_lines:
		cogs_line = hf.processCogListLine(line)
		cogs_data[cogs_line['COG_id']] = cogs_line
		es_cogs.append(es.index_op(cogs_line))

	es.bulk(es_cogs, index='cogs', doc_type='cogsObject')
	timedelta = datetime.now() - start
	print('COGs data was inserted to db in {}.'.format(timedelta))
	return cogs_data


def preprocess(taxa, cogs, strings):
	"""
	Preprocess data sent by user
	:param taxa: the taxa file
	:param cogs: the cogs file
	:param strings: the strings file
	"""
	taxa_data = preprocessTaxa(taxa)
	cogs_data = preprocessCogs(cogs)
	preprocessStrings(strings, taxa_data, cogs_data)


if __name__ == "__main__":
	if len(sys.argv) < 4:
		print('Not enough arguments!')

	else:
		args = sys.argv[1:]
		files = hf.open_file([sys.argv[1], sys.argv[2], sys.argv[3]])
		preprocess(files['taxa'], files['cogs'], files['strings'])
