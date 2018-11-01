import pandas as pd
import numpy as np
import random

class TravellingSalesman:
	def __init__(self, cities: list, cities_routes: dict = {}):
		self.__cities = cities
		self.__cities_routes = {}

		self.__population = []
		self.__population_city_score = []
		self.__population_distance_score = []
		
		self.__head = 20
		self.__chance_route = 0.5
		self.__mutation_chance = 0.1
		self.__total_population = 100

		if len(cities) == 0:
			self.__GenerateCities()
		else:
			self.__cities = cities

		if len(cities_routes) == 0 :
			self.__GenerateRoutes()
		else:
			self.__cities_routes = cities_routes

	def Execute(self):
		return

	def __GenerateCities(self):
		#Create the indexes and initialize the lists in each
		for i in random.randrange(0, 20):
			self.__cities.append(str(i))

	def __GenerateRoutes(self):
		#Create the indexes and initialize the lists in each
		for city in self.__cities:
			self.__cities_routes[city] = []
		
		#For each city (1)
		for city in self.__cities:
			#For each city (2)
			for temp in self.__cities:
				#If it's not the same city
				if city != temp:
					#if the city (1) don't have a route to the city (2) yet, and a route  
					if temp not in self.__cities_routes[city] and random.random() <= self.__chance_route:
						distance = random.randrange(0, 10)
						self.__cities_routes[city].append({temp: distance})
						self.__cities_routes[temp].append({city: distance})

		#This loop is to ensure there is no city alone
		for city in self.__cities:
			#If the city don't have route to other cities
			if len(self.__cities_routes[city]) == 0:
				#Choose a random city to create a route
				temp = random.randrange(0, len(self.__cities))
				temp = self.__cities[temp]
				#Stabilish the route
				self.__cities_routes[city].append({temp: distance})
				self.__cities_routes[temp].append({city: distance})

	def __NewGeneration(self):
		

a = TravellingSalesman()
