from pytrie import SortedStringTrie as Trie


class Algorithm:
	def __init__(self, size, string):
		self.sigmaSize = size
		self.string = string
		self.stringLength = len(string)
		self.trie = Trie()

	def run(self):
		for k in range(self.stringLength):
			self.initialize(k+1)

	def initialize(self, k):
		left = 1
		right = 0
		number = 0
		counter = [0 for x in range(self.sigmaSize + 1)]
		life = [0 for x in range(self.sigmaSize + 1)]

		while number < k and right < self.stringLength:
			right += 1
			index = int(self.string[right-1])
			counter[index] += 1
			if counter[index] == 1:
				number += 1
				life[index] = 1

		if right == self.stringLength and number < k:
			return

		self.handle_fingerprint(life)
		self.main(k, number, right, left, counter, life)

	def main(self, k, number, right, left, counter, life):
		while right < self.stringLength:
			while number < k + 1 and right < self.stringLength:
				right += 1
				index = int(self.string[right-1])
				counter[index] += 1
				if counter[index] == 1:
					number += 1
					life[index] = 1

			if right == self.stringLength and number <= k:
				return

			while number > k:
				index = int(self.string[left-1])
				counter[index] -= 1
				if counter[index] == 0:
					number -= 1
					life[index] = 0

				left += 1


			self.handle_fingerprint(life)

	def handle_fingerprint(self, life):
		fingerprint = ''
		for x in range(self.sigmaSize + 1):
			if life[x] == 1:
				fingerprint += str(x)

		if fingerprint in self.trie.keys():
			self.trie[[fingerprint]] += 1

		else:
			self.trie[[fingerprint]] = 1

	def print_fingerprints(self):
		print(self.trie)




