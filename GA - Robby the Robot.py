'''
13/06/2018 - Wander Damasceno Rodrigues
Genetic Algorithm to use in "Robby, the robot" problem using pandas and numpy
'''

from math import floor
import random
import pandas as pd
import numpy as np

class GA:
	def __init__(self: str):
		data = {'Data': [], 'Fitness': []}
		self.__population = pd.DataFrame(data=data)
		self.__total_population = 200
		self.__generation = 1
		self.__world = []
		
		self.__total_worlds = 100
		self.__size_world = 10
		self.__thrash_chance = 0.2
		self.__total_movements = 250
		self.__total_actions = 5
		self.__pos_x = 0
		self.__pos_y = 0
		
		self.__point_thrash = 10
		self.__point_no_thrash = -1
		self.__point_wall = -5

		self.__head = 20
		self.__mutation_chance = 0.005
		self.__total_generation = 500

		self.__world = [[[0] * self.__size_world] * self.__size_world] * self.__total_worlds

	def Execute(self):
		#Generate the world
		self.__GenerateWorld()
		#Until the last generation
		while self.__generation <= self.__total_generation:
			#Create the new generation
			self.__NewGeneration()
			#Get the best population
			self.__GetBestPopulation()
			print('Generation {generation} ({fitness}):\n{data}\n'.format(generation=self.__generation, fitness=self.__population.iloc[0]['Fitness'], data=self.__population.iloc[0]['Data']))
			self.__generation += 1

	def __GenerateWorld(self):
		#Run the worlds and add thrash
		for i in range(self.__total_worlds):
			for j in range(self.__size_world):
				for k in range(self.__size_world):
					self.__world[i][j][k] = 1 if random.random() <= self.__thrash_chance else 0

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
				movements = np.random.randint(0, self.__total_actions, self.__total_movements)
				data.append(movements)
				fitness.append(0)

			#Add the elements generated to the population
			self.__population = pd.concat([self.__population, pd.DataFrame(data={'Data': data, 'Fitness': fitness})])
		else:
			self.__Breed()

		#Calculate the fitness of each element
		self.__population['Fitness'] = self.__population['Data'].apply(lambda x: self.__Fitness(x))

	def __Fitness(self, actions):
		'''
		Run the actual world
		Action list:
			0: walk up
			1: walk right
			2: walk down
			3: walk left
			4: grab thrash
		'''
		fitness = 0
		#For each world
		for i in range(self.__total_worlds):
			pos_x = self.__pos_x
			pos_y = self.__pos_y
			#For each action
			for j in actions:
				#If walking up
				if j == 0:
					#Check the wall or walk
					if pos_x == 0:
						fitness += self.__point_wall
					else:
						pos_x -= 1
				#If walking right
				elif j == 1:
					#Check the wall or walk
					if pos_y == self.__size_world - 1:
						fitness += self.__point_wall
					else:
						pos_y += 1
				#If walking down
				elif j == 2:
					#Check the wall or walk
					if pos_x == self.__size_world - 1:
						fitness += self.__point_wall
					else:
						pos_x += 1
				#If walking left
				elif j == 3:
					#Check the wall or walk
					if pos_y == 0:
						fitness += self.__point_wall
					else:
						pos_y -= 1
				#If trying to grab thrash
				elif j == 4:
					if self.__world[i][pos_x][pos_y] == 1:
						fitness += self.__point_thrash
						self.__world[i][pos_x][pos_y] = 0
					else:
						fitness += self.__point_no_thrash 
					

		return fitness

	def __GetBestPopulation(self):
		'''
		Order by the column Fitness in descending order
		Get the first 20 rows of the DataFrame
		'''
		self.__population = self.__population.sort_values(by='Fitness', ascending=0)
		self.__population = self.__population.head(self.__head)

	def __Mutation(self, actions: list):
		'''
		For each element in item, see if it will mutate
		If mutate, choose a new element to replace
		'''
		count = 0
		for i in actions:
			if random.random() <= self.__mutation_chance:
				actions[count] = random.randrange(0, self.__total_actions)
			count += 1
		return actions
		
	def __Breed(self):
		temp_population = pd.DataFrame(data={'Data': [], 'Fitness': []})
		
		#While the population didn't reached the max, continue breeding
		while len(self.__population) + len(temp_population) < self.__total_population:
			#Choose the two elements to breed
			itens = [random.randrange(0, self.__head), random.randrange(0, self.__head)]
			
			#Define the crossover point
			local = np.random.randint(0, self.__total_movements)

			#Generate the new elements
			a = np.concatenate([self.__population.iloc[itens[0]]['Data'][:local], self.__population.iloc[itens[1]]['Data'][local:]])
			b = np.concatenate([self.__population.iloc[itens[1]]['Data'][:local],  self.__population.iloc[itens[0]]['Data'][local:]])
			#Do the mutation
			a = self.__Mutation(a)
			b = self.__Mutation(b)

			#Concatenate the new elements in the temp population
			data = {'Data': [a, b], 'Fitness': [self.__Fitness(a), self.__Fitness(b)]}
			data = pd.DataFrame(data=data)
			temp_population = pd.concat([temp_population, data])

		#Throw the actual population away and use just the breeded population
		self.__population = temp_population

ga = GeneticAlgorithm('Hello World!')
ga.Execute()