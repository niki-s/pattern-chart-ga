import random
import numpy as np

class Individual(object):
	"""docstring for individual"""
	def __init__(self, numcolors):
		self.numcolors = numcolors
		self.numrules = (3*numcolors)-2
		self.fitness = 0
		#self.chrom = np.random.randint(numcolors, size=(4))
		self.fillColor = 0#np.random.randint(numcolors)
		self.chrom = np.random.randint(numcolors, size=(4*self.numrules))
		self.label = 0

	# def initRandom(self, inlist):
	# 	# create a new chromosome with random values
	# 	for i in range(self.numrules):
	# 		self.chrom = np.random.randint(numcolors, size=(4*numrules))
		