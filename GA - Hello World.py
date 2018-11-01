'''
13/06/2018 - Wander Damasceno Rodrigues
Genetic Algorithm to make a specific word using pandas and numpy
'''

from math import floor
import random
import pandas as pd
import numpy as np

class GeneticAlgorithm:
	def __init__(self, model: str):
		#Do not change those variables
		self.__model = model
		self.__population = pd.DataFrame(data={'Data': [], 'Fitness': []})
		self.__generation = 1
		
		#You can change the above variables
		self.__head = 20
		self.__mutation_chance = 0.05
		self.__total_population = 100
		self.__list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ! '

	def Execute(self):
		while True:
			#Create the new generation
			self.__NewGeneration()
			#Get the best population
			self.__GetBestPopulation()
			#Show only the first line within the best part of population
			print('Generation {generation}: {data} ({fitness})'.format(generation=self.__generation, fitness=self.__population.iloc[0]['Fitness'], data=self.__population.iloc[0]['Data']))
			#Stop the algorithm if the word is achieved
			if self.__population.iloc[0]['Fitness'] == 1:
				break
			self.__generation += 1
		print('Word formed at generation {generation}!'.format(generation=self.__generation))


	def __NewGeneration(self):
		'''
		If it's the first generation, generate random elements
		If it's not, breed
		'''
		if self.__generation == 1:
			data = []
			fitness = []
			#Generate random elements
			for i in range(self.__total_population):
				element = ''
				for j in range(len(self.__model)):
					element = element + random.choice(self.__list)
				#Add to population
				data.append(element)
				fitness.append(0)
			self.__population = pd.concat([self.__population, pd.DataFrame(data={'Data': data, 'Fitness': fitness})])
		else:
			self.__Breed()

		#Calculate the fitness of each element
		self.__population['Fitness'] = self.__population['Data'].apply(lambda x: self.__Fitness(x))

	def __Fitness(self, element):
		'''
		Compare the element with the model.
		1 -> Exactly
		0 -> Completely different
		'''
		length = len(self.__model)
		equal = 0
		count = 0
		for char in element:
			if char == self.__model[count]:
				equal += 1
			count += 1
		return equal / length

	def __GetBestPopulation(self):
		'''
		Order by the column Fitness in descending order
		Get the first 20 rows of the DataFrame
		'''
		self.__population = self.__population.sort_values(by='Fitness', ascending=0)
		self.__population = self.__population.head(self.__head)

	def __Mutation(self, item: str):
		'''
		For each element in item, see if it will mutate
		If mutate, choose a new element to replace
		'''
		count = 0
		characters = list(item)
		for i in characters:
			if random.random() <= self.__mutation_chance:
				characters[count] = random.choice(self.__list)
			count += 1
		return ''.join(characters)
		
	def __Breed(self):
		#Create a temporary data frame
		temp_population = pd.DataFrame(data={'Data': [], 'Fitness': []})
		
		#While the population didn't reached the max, continue breeding
		while len(self.__population) + len(temp_population) < self.__total_population:
			#Choose the two elements to breed
			itens = [random.randrange(0, self.__head), random.randrange(0, self.__head)]
			
			#Define the center of the model
			local = np.random.randint(0, len(self.__model))

			#Generate the new elements
			a = self.__population.iloc[itens[0]]['Data'][:local] + self.__population.iloc[itens[1]]['Data'][local:]
			b = self.__population.iloc[itens[1]]['Data'][:local] + self.__population.iloc[itens[0]]['Data'][local:]
			#Do the mutation
			a = self.__Mutation(a)
			b = self.__Mutation(b)

			#Concatenate the new elements in the temp population
			data = {'Data': [a, b], 'Fitness': [self.__Fitness(a), self.__Fitness(b)]}
			data = pd.DataFrame(data=data)
			temp_population = pd.concat([temp_population, data])

		#Merge the population with the breeded population
		self.__population = pd.concat([self.__population, temp_population])

ga = GeneticAlgorithm('Hello World!')
ga.Execute()