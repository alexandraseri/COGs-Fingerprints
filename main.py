import sys
from algorithm import Algorithm
import Preprocess as pp
import HelperFunctions as hf


def runAlgorithm(family):
	sigma = hf.getFamilySigma(family)
	strings = hf.getFamilyStrings(family)
	algorithm = Algorithm(sigma, strings)
	algorithm.run()

options = {
	'-pTaxa': {
		'function': pp.preprocessTaxa,
		'numOfArgs': 1
	},
	'-pSigma': {
		'function': pp.preprocessSigma,
		'numOfArgs': 1
	},
	'-r': {
		'function': runAlgorithm,
		'numOfArgs': 1
	}
}

def argInOption(arg):
	if arg not in options:
		print 'You have to provide a valid option: {}. You provided {}.'.format(options.keys().join(', '), arg)
		return False

	return options[arg]

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print 'Not enough arguments!'

	else:
		args = sys.argv[1:]
		first = argInOption(args[0])
		if first and len(args) > first['numOfArgs']:
			options[args[0]]['function'](args[1:first['numOfArgs'] + 1])

			if len(args) > first['numOfArgs'] + 1:
				second = argInOption(args[first['numOfArgs'] + 1])

				if second and len(args[first['numOfArgs'] + 1:]) > second['numOfArgs']:
					options[args[first['numOfArgs'] + 1]]['function'](args[first['numOfArgs'] + 2:first['numOfArgs'] + second['numOfArgs'] + 2])

					if len(args) > first['numOfArgs'] + second['numOfArgs'] + 2:
						third =	argInOption(args[first['numOfArgs'] + second['numOfArgs'] + 2])

						if third and len(args[first['numOfArgs'] + second['numOfArgs'] + 2]) > third['numOfArgs']:
							options[args[first['numOfArgs'] + second['numOfArgs'] + 2]]['function'](args[first['numOfArgs'] + second['numOfArgs'] + 3:first['numOfArgs'] + second['numOfArgs'] + third['numOfArgs'] + 2])

	# else:
	# 	# Assumption: SIGMA = {1....|SIGMA|}
	# 	string = str(sys.argv[1])
	# 	size = sizeOfSigma(string)
	# 	print('Sigma size is {} and string is {}'.format(size, string))
	#
	# 	# Run Algorithm
	# 	algorithm = Algorithm(size, string)
	# 	algorithm.run()
	# 	algorithm.print_fingerprints()

