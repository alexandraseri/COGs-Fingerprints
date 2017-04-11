import HelperFunctions as hf

class Algorithm:
	def __init__(self, sigma, strings):
		self.sigma = sigma
		self.stringList = strings
		self.fingerPrints = {}

	def run(self):
		for i in range(len(self.stringList)):
			string = self.stringList[i]
			for k in range(len(string['string'].split(';'))):
				self.initialize(k+1, string)

	def initialize(self, k, string):
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
		with open('fingerprints.txt','w+') as file:
			for key in self.fingerPrints.keys():
				file.write('----> fingerprint: {} \n --------> in strings: {}. \n'.format(key, ', '.join(self.fingerPrints[key])))




