import random
from random import shuffle
import math
import sys
import pickle
from individual import Individual
import numpy as np
import os.path
import time

# CHROMSIZE_ROW = 5
# CHROMSIZE_COL = 5
NUMCOLORS = 2
POPSIZE = 30
GENERATIONS = 5
SEED = 41
CASIZE = 25
seedRow = []

def initPop():
	population = []
	for i in range(POPSIZE):
		ind = Individual(NUMCOLORS)
		population.append(ind)
	return population

def evaluate(indexes, population):
	# get the fitness of each individual in the population
	# do user input here
	currentFile = 0
	for i in indexes:
		# first make a CA from each of the individual's rules
		generateCA(population[i].chrom, str(currentFile))
		currentFile += 1

	# then wait for the appropriate feedback file to get created
	while not os.path.exists("/home/niki/Downloads/result.txt"):
		print "waiting for feedback"
		time.sleep(1)

	print "GOT RESULTS"
	f = open("/home/niki/Downloads/result.txt", 'r')
	fitnessUpdates = f.read()
	fitnessUpdates = fitnessUpdates.strip().split(',')
	# print fitnessUpdates
	fitIndex = 0

	countSelected = indexes.count(1)
	reward = 5./max(float(countSelected), 1.)

	for i in indexes:
		if int(fitnessUpdates[fitIndex]) == 1:
			population[i].fitness += reward
		else:
			population[i].fitness/4.

		print fitIndex, population[i].fitness
		fitIndex += 1

	for i, individual in enumerate(population):
		if i not in indexes:
			individual.fitness/2.

	f.close()
	os.remove("/home/niki/Downloads/result.txt")

def crossover(Px, Pm, p1, p2, p1Fit, p2Fit):
	# make children with appropriate length
	child1 = [0] * len(p1)
	child2 = [0] * len(p2)

	#if doWithProb returns true, perform crossover
	if doWithProb(Px):
		index = random.randint(0, (3**NUMCOLORS))

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
		avgPFit = (p1Fit + p2Fit)/2
		return np.asarray(child1), np.asarray(child2), avgPFit, avgPFit

	else:
		child1[:] = p1[:]
		child2[:] = p2[:]

		if doWithProb(Pm):
			mutate(child1)
		if doWithProb(Pm):
			mutate(child2)

		# print "no crossover"
		avgPFit = (p1Fit + p2Fit)/2
		return np.asarray(child1), np.asarray(child2), avgPFit, avgPFit

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

def avgFitness(population):
	totalFit = 0.0
	for individual in population:
		totalFit += individual.fitness

	return totalFit/float(POPSIZE)

def maxFitness(population):
	currentMax = 0
	for individual in population:
		if individual.fitness > currentMax:
			currentMax = individual.fitness

	return currentMax

def generateCA(testrules, outfile):
	#testrules = [1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0]
	defaultColor = 0
	ruleset = [testrules[i:i + 4] for i in xrange(0, len(testrules), 4)]
	#print ruleset

	#seedRow = [0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]#np.random.randint(2, size=(16))
	# seedRow = np.random.randint(3, size=(15))
	mat = np.zeros((CASIZE,CASIZE), dtype=np.int)
	mat[0] = seedRow


	# fill the remainder of the mat values according to the rules
	for i in range(CASIZE):
		for j in range(CASIZE):
			if i !=0:	#skip first row because it's been set already
				if j == 0 or j == CASIZE-1:
					mat[i][j] = defaultColor
				else:
					for rule in ruleset:
						previousLine = mat[i-1][j-1:j+2]
						test = rule[1:]
						# print previousLine[0], test[0]
						# print previousLine[1], test[1]
						# print previousLine[2], test[2]
						if (previousLine[0] == test[0]) and (previousLine[1] == test[1]) and (previousLine[2] == test[2]):
							mat[i][j] = rule[0]

	# print outfile
	f = open("./GA/app/Patterns/"+outfile+".txt", 'w+')
	for i in range(CASIZE):
		for j in range(CASIZE):
			f.write(str(mat[i][j]))
		f.write('\n')
	f.close()

def fitnessPropSelectSubset(pop,numselect):
	for ind in pop:
		sumFit = ind.fitness

	avgFit = sumFit/len(pop)

	sumExpected = 0
	for ind in pop:
		ind.expectedFitness = ind.fitness / avgFit
		sumExpected += ind.expectedFitness

	subset = []
	for i in range(numselect):
		G = random.uniform(0,sumExpected)
		select = 0

		for i, ind in enumerate(pop):
			select += ind.expectedFitness

			if select >= G:
				subset.append(i)
				break

	#pop.sort(key=lambda individual:individual.fitness, reverse=True)
	print subset
	return subset
	#return [0,1,2,3,4,5,6,7,8,9,10,11]

def main():	
	random.seed(SEED)
	Px = .8
	Pm = .3
	outData = []
	global seedRow
	seedRow = np.random.randint(NUMCOLORS, size=(CASIZE))

	# create initial population with random strings
	pop = initPop()

	# test print
	# for ind in pop:
	# 	print ind.chrom

	#get fitnesses for population
	# evaluate(pop)
	# for ind in pop:
	# 	print ind.fitness

	# # reproduce, double population via random selection and etc, for each generation
	for i in range(GENERATIONS):
		#print "Gen:", i
		#crossover double pop
		for j in range(POPSIZE/2):
			# parent1 = getRandomIndividual(pop)
			# parent2 = getRandomIndividual(pop)
			index1 = fitnessPropSelectSubset(pop,1)[0]
			index2 = fitnessPropSelectSubset(pop,1)[0]
			parent1 = pop[index1]
			parent2 = pop[index2]
			child1 = Individual(NUMCOLORS)
			child2 = Individual(NUMCOLORS)
			child1.chrom, child2.chrom, child1.fitness, child2.fitness = crossover(Px, Pm, parent1.chrom, parent2.chrom, parent1.fitness, parent2.fitness)

			# add new children to population
			# del pop[index1]
			pop.remove(parent1)
			if parent2 in pop:	#could have been the same as parent1
				pop.remove(parent2)
			pop.append(child1)
			pop.append(child2)

			#print len(pop)
		# eval new members of population
		subset = fitnessPropSelectSubset(pop,12)
		evaluate(subset, pop)

		# sort pop in place based on highest fitness
		#pop.sort(key=lambda individual:individual.fitness, reverse=True)

		# print "more before cull"
		# for ind in pop:
		# 	print ind.fitness

		# remove excess population
		#pop[POPSIZE:] = []
		# print "aftercull"
		# for ind in pop:
		# 	print ind.fitness

	# 	# append new generation info to out data
		print i
		genInfo = [i, avgFitness(pop), maxFitness(pop)]
	# 	if i % 50 == 0:
	# 		print genInfo

		outData.append(genInfo)

	pickle.dump(outData, open("saveFile", 'w+'))

	# for ind in pop:
	# 	print ind.fitness
	pop.sort(key=lambda individual:individual.fitness, reverse=True)
	for i in pop:
		print i.fitness
	print "top individual"
	print pop[0].chrom

if __name__ == '__main__':
	main()