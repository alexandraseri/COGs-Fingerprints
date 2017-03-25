import sys
from algorithm import Algorithm


def sizeOfSigma(string):
	sigma = set(string)
	return len(sigma)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print('Too few argumants. You have to give a string as input!')

	else:
		# Assumption: SIGMA = {1....|SIGMA|}
		string = str(sys.argv[1])
		size = sizeOfSigma(string)
		print('Sigma size is {} and string is {}'.format(size, string))

		# Run Algorithm
		algorithm = Algorithm(size, string)
		algorithm.run()
		algorithm.print_fingerprints()

