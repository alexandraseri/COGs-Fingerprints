def getAboveThreshold(threshold, minNumber,  fingerprints, family):
	"""
	Get all results above certain threshold number and write them to files in results folder.
	:param threshold: the requested % of the strings with the same fingerprint.
	:param minNumber: the requested minimum number of strings with the same fingerprint.
	:param fingerprints: the fingerprints object
	:param family: the strings's family.
	"""
	with open('results/' + family + '_fingerprint_' + str(threshold) + '.txt', 'w+') as file:
		for key in fingerprints.keys():
			if len(fingerprints[key]) > minNumber:
				file.write('--- Fingerprint: {} \n------in strings: {}. \n'.format(key, ', '.join(fingerprints[key])))