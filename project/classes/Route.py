#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABC, abstractmethod

class Route(ABC):
	@abstractmethod
	def calculateEffort(self):
		"""@ReturnType Integer"""
		pass

	def getName(self):
		"""@ReturnType String"""
		return self.___name

	def setName(self, aName):
		"""@ParamType aName String
		@ReturnType void"""
		self.___name = aName

	def getLocation(self):
		"""@ReturnType GymInfo"""
		return self.___location

	def setLocation(self, aLocation):
		"""@ParamType aLocation GymInfo
		@ReturnType void"""
		self.___location = aLocation

	def getHolds(self):
		return self.___holds

	def setHolds(self, aHolds):
		"""@ReturnType void"""
		self.___holds = aHolds

	def getActualDifficulty(self):
		"""@ReturnType Integer"""
		return self.___actualDifficulty

	def setActualDifficulty(self, aActualDifficulty):
		"""@ParamType aActualDifficulty Integer
		@ReturnType void"""
		self.___actualDifficulty = aActualDifficulty

	def getFeltDifficulty(self):
		"""@ReturnType Integer"""
		return self.___feltDifficulty

	def setFeltDifficulty(self, aFeltDifficulty):
		"""@ParamType aFeltDifficulty Integer
		@ReturnType void"""
		self.___feltDifficulty = aFeltDifficulty

	def __init__(self, name, location, holds, actualDifficulty, feltDifficulty):
		self.___name = name
		"""@AttributeType String"""
		self.___location = location
		"""@AttributeType GymInfo"""
		self.___holds = holds
		"""@AttributeType ArrayList"""
		self.___actualDifficulty = actualDifficulty
		"""@AttributeType Integer"""
		self.___feltDifficulty = feltDifficulty
		"""@AttributeType Integer"""
	
class TopRope(Route):
	def calculateEffort(self):
		"""@ReturnType Integer"""
		pass

class Bouldering(Route):
	def calculateEffort(self):
		"""@ReturnType Integer"""
		pass

class Lead(Route):
	def calculateEffort(self):
		"""@ReturnType Integer"""
		pass

