import HelperFunctions as hf

class Algorithm:
	def __init__(self, sigma, strings):
		self.sigma = sigma
		self.stringList = strings
		self.fingerPrints = {}

	def run(self):
		for i in range(len(self.stringList)):
			string = self.stringList[i]
			for k in range(len(string['string'])):
				self.initialize(k+1, string)

	def initialize(self, k, string):
		left = 1
		right = 0
		number = 0
		life = hf.createLife(string['id'], self.sigma)
		while number < k and right < len(string['string']):
			right += 1
			letter = string['string'][right-1]
			life['letters'][letter] += 1
			if life['letters'][letter] == 1:
				number += 1

		if right == len(string['string']) and number < k:
			return

		self.handle_fingerprint(life)
		self.main(string, k, number, right, left, life)

	def main(self, string, k, number, right, left, life):
		while right < len(string['string']):
			while number < k + 1 and right < len(string['string']):
				right += 1
				letter = string['string'][right-1]
				life['letters'][letter] += 1
				if life['letters'][letter] == 1:
					number += 1

			if right == len(string['string']) and number <= k:
				return

			while number > k:
				letter = string['string'][left-1]
				life['letters'][letter] -= 1
				if life['letters'][letter] == 0:
					number -= 1

				left += 1


			self.handle_fingerprint(life)

	def handle_fingerprint(self, life):
		fingerprint = []
		letters =life['letters'].keys()
		for letter in letters:
			if life['letters'][letter] > 0 :
				fingerprint.append(letter)

		key = fingerprint.join(';')
		if key not in self.fingerPrints:
			self.fingerPrints[key] = []

		self.fingerPrints[key].append(life['string'])

	def print_fingerprints(self):
		for key in self.fingerPrints.keys():
			print '----> fingerprint: {} \n --------> in strings: {}. \n\n'.format(key, self.fingerPrints[key].join(', '))




