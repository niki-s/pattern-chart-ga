import random
import numpy as np

class PatternIndividual(object):
	"""docstring for individual"""
	def __init__(self, chromSizeRow, chromSizeCol):
		self.chromSizeRow = chromSizeRow
		self.chromSizeCol = chromSizeCol
		self.fitness = 0
		self.chrom = np.random.randint(2, size=(chromSizeRow, chromSizeCol))
		

	def initRandom(self, inlist):
		# create a new chromosome with a 
		self.chrom = np.random.randint(2, size=(chromSizeRow, chromSizeCol))
		