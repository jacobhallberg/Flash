from abc import ABC, abstractmethod

class Route(ABC):
	@abstractmethod
	def calculateEffort(self):
		pass

	def getName(self):
		return self.___name

	def getLocation(self):
		return self.___location

	def getHolds(self):
		return self.___holds

	def getActualDifficulty(self):
		return self.___actualDifficulty

	def getFeltDifficulty(self):
		return self.___feltDifficulty

	def __init__(self, name, location, holds, actualDifficulty, feltDifficulty):
		self.___name = name
		self.___location = location
		self.___holds = holds
		self.___actualDifficulty = actualDifficulty
		self.___feltDifficulty = feltDifficulty
	
class TopRope(Route):
	required_climbers = 2
	gear_required = True

	def calculateEffort(self):
		return 0


class Bouldering(Route):
	required_climbers = 1
	gear_required = False
	
	def calculateEffort(self):
		return 0

class Lead(Route):
	required_climbers = 2
	gear_required = True

	def calculateEffort(self):
		return 0

