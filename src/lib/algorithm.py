import HelperFunctions as hf


class Algorithm:
	"""
	The Algorithm based on the article.
	"""
	def __init__(self, sigma, strings, family):
		"""
		Algorithm constructor
		:param sigma: the sigma for this run of the algorithm.
		:param strings: the strings to process.
		:param family: the family those strings are from for documenting purposes.
		"""
		self.family = family
		self.sigma = sigma
		self.stringList = strings
		self.fingerPrints = {}

	def run(self):
		"""
		Run the algorithm.
		"""
		for i in range(len(self.stringList)):
			string = self.stringList[i]
			for k in range(len(string['string'].split(';'))):
				self.initialize(k+1, string)

	def initialize(self, k, string):
		"""
		Initialize fingerprint. Based on the article.
		:param k: the wanted size of the fingerprint.
		:param string: the string to analyze.
		:return: If no initial fingerprint found, stop the algorithm.
		"""
		left = 1
		right = 0
		number = 0
		life = hf.createLife(string['name'], self.sigma)
		while number < k and right < len(string['string'].split(';')):
			right += 1
			letter = string['string'].split(';')[right-1]
			life['letters'][letter] += 1
			if life['letters'][letter] == 1:
				number += 1

		if right == len(string['string'].split(';')) and number < k:
			return

		self.handle_fingerprint(life)
		self.main(string, k, number, right, left, life)

	def main(self, string, k, number, right, left, life):
		"""
		Main part of the algorithm, based on the article.
		:param string: the string to analyze.
		:param k: the wanted size of the fingerprint.
		:param number: the current size of the fingerprint.
		:param right: rightmost index for this run.
		:param left: leftmost index for this run.
		:param life: the string's object counting the number of occurrences for each COG.
		:return: if no fingerprint found, stop the algorithm.
		"""
		while right < len(string['string'].split(';')):
			while number < k + 1 and right < len(string['string'].split(';')):
				right += 1
				letter = string['string'].split(';')[right-1]
				life['letters'][letter] += 1
				if life['letters'][letter] == 1:
					number += 1

			if right == len(string['string'].split(';')) and number <= k:
				return

			while number > k:
				letter = string['string'].split(';')[left-1]
				life['letters'][letter] -= 1
				if life['letters'][letter] == 0:
					number -= 1

				left += 1

			self.handle_fingerprint(life)

	def handle_fingerprint(self, life):
		"""
		Saving the fingerprint in fingerprints object.
		:param life: the string's object counting the number of occurrences for each COG.
		"""
		fingerprint = []
		letters =life['letters'].keys()
		for letter in letters:
			if life['letters'][letter] > 0 :
				fingerprint.append(letter)

		fingerprint.sort()

		key = ';'.join(fingerprint)
		if key not in self.fingerPrints:
			self.fingerPrints[key] = []

		self.fingerPrints[key].append(life['string'])

	def print_fingerprints(self):
		"""
		Save fingerprint file in results folder, containing all the fingerprints found in the algorithm run.
		"""
		with open('results/' + self.family + '_fingerprints.txt', 'w+') as file:
			for key in self.fingerPrints.keys():
				file.write('----> fingerprint: {} \n --------> in strings: {} \n'.format(key, ', '.join(self.fingerPrints[key])))
