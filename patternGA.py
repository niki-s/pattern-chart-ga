import random
import math
import sys
import pickle
from individual import Individual
import numpy as np

# CHROMSIZE_ROW = 5
# CHROMSIZE_COL = 5
NUMCOLORS = 2
POPSIZE = 5
GENERATIONS = 4
SEED = 41

def initPop():
	population = []
	for i in range(POPSIZE):
		ind = Individual(NUMCOLORS)
		population.append(ind)
	return population

def evaluate(population):
	# get the fitness of each individual in the population
	# do user input here
	currentFile = 0
	for individual in population:
		# first make a CA from each of the individual's rules
		generateCA(individual.chrom, str(currentFile))
		currentFile += 1

	# then wait for feedback and update fitness
	for individual in population:
		individual.fitness = random.randint(0,10)
		#return True
def crossover(Px, Pm, p1, p2):
	# make children with appropriate length
	child1 = [0] * len(p1)
	child2 = [0] * len(p2)

	#if doWithProb returns true, perform crossover
	if doWithProb(Px):
		index = random.randint(0, (3*NUMCOLORS)-2)

		child1[0:index] = p1[0:index]
		child1[index:] = p2[index:]
		child2[0:index] = p2[0:index]
		child2[index:] = p1[index:]

		#print "children", child1, child2, "from", p1, p2, "with index", index

		if doWithProb(Pm):
			mutate(child1)
		if doWithProb(Pm):
			mutate(child2)
		# print "children with maybe mutation", child1, child2
		return np.asarray(child1), np.asarray(child2)

	else:
		child1[:] = p1[:]
		child2[:] = p2[:]

		if doWithProb(Pm):
			mutate(child1)
		if doWithProb(Pm):
			mutate(child2)

		# print "no crossover"
		return np.asarray(child1), np.asarray(child2)

def mutate(chrom):
	flip = random.randint(0, 3)
	chrom[flip] = random.randint(0, NUMCOLORS-1)

def doWithProb(prob):
	# random.random returns a number between 0 and 1, returns true if generated # is < input probability
	if random.random() < prob:
		return True
	else:
		return False

def getRandomIndividual(population):
	ind = random.randint(0, POPSIZE-1)
	return population[ind]

def generateCA(testrules, outfile):
	#testrules = [1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0]
	defaultColor = 0
	ruleset = [testrules[i:i + 4] for i in xrange(0, len(testrules), 4)]
	#print ruleset

	seedRow = [1,0,0,1,0,1,0,1,1,0]#np.random.randint(2, size=(10))
	mat = np.zeros((10,10), dtype=np.int)
	mat[0] = seedRow

	# fill the remainder of the mat values according to the rules
	for i in range(10):
		for j in range(10):
			if i !=0:	#skip first row because it's been set already
				if j == 0 or j == 9:
					mat[i][j] = defaultColor
				else:
					for rule in ruleset:
						previousLine = mat[i-1][j-1:j+2]
						test = rule[1:]
						if (previousLine[0] == test[0]) and (previousLine[1] == test[1]) and (previousLine[2] == test[2]):
							mat[i][j] = rule[0]

	print mat
	f = open(outfile, 'w+')
	for i in range(10):
		for j in range(10):
			f.write(str(mat[i][j]))
		f.write('\n')
	f.close()

def main():	
	random.seed(SEED)
	Px = .8
	Pm = .3

	# create initial population with random strings
	pop = initPop()

	# test print
	for ind in pop:
		print ind.chrom

	#get fitnesses for population
	evaluate(pop)
	for ind in pop:
		print ind.fitness

	# # reproduce, double population via random selection and etc, for each generation
	for i in range(GENERATIONS):
		#print "Gen:", i
		#crossover double pop
		for j in range(POPSIZE):
			parent1 = getRandomIndividual(pop)
			parent2 = getRandomIndividual(pop)
			child1 = Individual(NUMCOLORS)
			child2 = Individual(NUMCOLORS)
			child1.chrom, child2.chrom = crossover(Px, Pm, parent1.chrom, parent2.chrom)

			# add new children to population
			pop.append(child1)
			pop.append(child2)

			#print len(pop)
		# eval new members of population
		evaluate(pop)

		# sort pop in place based on highest fitness
		pop.sort(key=lambda individual:individual.fitness, reverse=True)

		# print "more before cull"
		# for ind in pop:
		# 	print ind.fitness

		# remove excess population
		pop[POPSIZE:] = []
		# print "aftercull"
		# for ind in pop:
		# 	print ind.fitness

	# 	# append new generation info to out data
	# 	genInfo = [i, minDistance(pop), avgDistance(pop), maxDistance(pop)]
	# 	if i % 50 == 0:
	# 		print genInfo

	# 	outData.append(genInfo)

	# pickle.dump(outData, open(saveFile, 'w'))

	# for ind in pop:
	# 	print ind.fitness


if __name__ == '__main__':
	main()