import random
import math
import sys
import pickle
from individual import PatternIndividual

CHROMSIZE_ROW = 5
CHROMSIZE_COL = 5
POPSIZE = 10
SEED = 999

def initPop():
	population = []
	for i in range(POPSIZE):
		ind = PatternIndividual(CHROMSIZE_ROW, CHROMSIZE_COL)
		population.append(ind)
	return population

def evaluate(population):
	# get the fitness of each individual in the population
	# do user input here
	pass
	for individual in population:
		#do stuff
		return True


def main():	
	random.seed(SEED)

	# create initial population with random strings
	pop = initPop()

	# test print
	for ind in pop:
		print ind.chrom

	# get fitnesses for population
	# evaluate(pop)


	# # reproduce, double population via random selection and etc, for each generation
	# for i in range(GENERATIONS):
	# 	#print "Gen:", i
	# 	#crossover double pop
	# 	for j in range(LAMBDA/2):
	# 		parent1 = getRandomIndividual(pop)
	# 		parent2 = getRandomIndividual(pop)
	# 		child1 = individual(CHROMSIZE)
	# 		child2 = individual(CHROMSIZE)
	# 		child1.chrom, child2.chrom = crossover(parent1.chrom, parent2.chrom)

	# 		# add new children to population
	# 		pop.append(child1)
	# 		pop.append(child2)

	# 	# eval new members of population
	# 	evaluate(pop)

	# 	# sort pop in place based on lowest distance (counts as highest fitness)
	# 	pop.sort(key=lambda individual:individual.fitness)

	# 	# print "more before cull"
	# 	# for ind in pop:
	# 	# 	print ind.fitness

	# 	# remove excess population
	# 	pop[POPSIZE:] = []
	# 	# print "aftercull"
	# 	# for ind in pop:
	# 	# 	print ind.fitness

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