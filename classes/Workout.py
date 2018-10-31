#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Workout(object):
	def getRoutes(self):
		return self.___routes

	def setRoutes(self, aRoutes):
		"""@ReturnType void"""
		self.___routes = aRoutes

	def getWorkoutName(self):
		"""@ReturnType String"""
		return self.___workoutName

	def setWorkoutName(self, aWorkoutName):
		"""@ParamType aWorkoutName String
		@ReturnType void"""
		self.___workoutName = aWorkoutName

	def __init__(self, routes, workoutName):
		self.___routes = routes
		"""@AttributeType Array"""
		self.___workoutName = workoutName
		"""@AttributeType String"""

