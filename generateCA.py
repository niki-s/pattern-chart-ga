import numpy as np

def generateCA(testrules, outfile):
	#testrules = [1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0]
	defaultColor = 0
	ruleset = [testrules[i:i + 4] for i in xrange(0, len(testrules), 4)]
	#print ruleset

	seedRow = np.random.randint(2, size=(15))
	mat = np.zeros((15,15), dtype=np.int)
	mat[0] = seedRow

	# fill the remainder of the mat values according to the rules
	for i in range(15):
		for j in range(15):
			if i !=0:	#skip first row because it's been set already
				if j == 0 or j == 14:
					mat[i][j] = defaultColor
				else:
					for rule in ruleset:
						previousLine = mat[i-1][j-1:j+2]
						test = rule[1:]
						if (previousLine[0] == test[0]) and (previousLine[1] == test[1]) and (previousLine[2] == test[2]):
							mat[i][j] = rule[0]

	print mat
	f = open(outfile, 'w+')
	for i in range(15):
		for j in range(15):
			f.write(str(mat[i][j]))
		f.write('\n')
	f.close()

def main():
	#generateCA([0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0], './0')
	# generateCA([1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0], './0')
	generateCA([0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0], './0')
if __name__ == '__main__':
	main()
