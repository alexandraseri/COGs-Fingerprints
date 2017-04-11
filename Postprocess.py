def getAboveThreshold(threshold, minNumber,  fingerprints, family):
	with open('results/' + family + '_fingerprint_' + str(threshold) + '.txt', 'w+') as file:
		for key in fingerprints.keys():
			if len(fingerprints[key]) > minNumber:
				file.write('--- Fingerprint: {} \n------in strings: {}. \n'.format(key, ', '.join(fingerprints[key])))