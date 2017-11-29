import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import pickle
from scipy import stats

# open directory that contains a list of output files
# read output files to lists and then avg things and do math
# finally use matplotlib to plot graphs
def main():

	outputs = []

	if len(sys.argv) < 1:
		print "please specify path to output files directory"
	else:
		path = sys.argv[1]

	filelist = os.listdir(path)

	for file in filelist:
		run = pickle.load(open(path+file, 'r'))
		outputs.append(run)
		#outputs.append(np.loadtxt(path+file))
			#print path+file

	#print outputs[0]
	# maxY = outputs[1][:, 3]
	# avgY = outputs[1][:, 2]
	# minY = outputs[1][:, 1]
	#outputs = outputs[0]
	gens = [item[0] for item in outputs[0]] #[item[0] for item in lst]
	# print "--------"
	#print gens
	
	# all Y's are distance related, so smaller is better
	maxY = []
	avgY = []
	# minY = []
	maxYs = []
	avgYs = []
	# minYs = []


	# rearrange data into plotable averages
	print len(gens), len(outputs)
	for gen in range(len(gens)):
		for run in range(len(outputs)):
			#print "gen, run", gen, run
			# minYs.append(outputs[run][gen][1])
			avgYs.append(outputs[run][gen][1])
			maxYs.append(outputs[run][gen][2])

		# minY.append(np.average(minYs))
		avgY.append(np.average(avgYs))
		maxY.append(np.average(maxYs))
		maxYs = []
		avgYs = []
		# minYs = []

	# for run in range(len(outputs)):
	# 	print outputs[run][0]
	finalMins = []
	for i in range(len(outputs)):
		finalMins.append(outputs[i][len(gens)-1][1])

	print "mean least distance", np.average(finalMins)
	print "least distance", np.min(finalMins)
	print "mode", stats.mode(finalMins)
	print "std", np.std(finalMins)

	#plt.plot(gens, maxY, 'r', gens, avgY, 'b', gens, minY, 'g')
	plt.plot(gens, avgY, 'b', gens, maxY, 'g')
	plt.title(path)
	plt.ylabel('fitness')
	plt.xlabel('generation')
	plt.show()

 

if __name__ == '__main__':
	main()