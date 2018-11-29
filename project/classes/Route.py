from abc import ABC, abstractmethod

class Route(ABC):
	""" The route class manages all aspects of a route object that a climber adds.
		The route class is an abstract class forcing subclasses to implement the 
		calculate_effort() method which is dependent on the type of route to be created.
    Parameters
    ----------
	name (str): The nane of the route.
	location (str): The location of the route.
	holds (Hold): Hold object with each hold found on the route.
	actual_difficulty (int): The rating given by the gym.
	felt_difficulty (int): The rating that the climber gives to the route.
    """
	@abstractmethod
	def calculate_effort(self):
		pass

	def get_name(self):
		return self.___name

	def get_location(self):
		return self.___location

	def get_holds(self):
		return self.___holds

	def get_actual_difficulty(self):
		return self.___actual_difficulty

	def get_felt_difficulty(self):
		return self.___felt_difficulty

	def __init__(self, name, location, holds, actual_difficulty, felt_difficulty):
		self.___name = name
		self.___location = location
		self.___holds = holds
		self.___actual_difficulty = actual_difficulty
		self.___felt_difficulty = felt_difficulty
	
class TopRope(Route):
	""" Child class that inherits from Route. Implements the calculate_effort() method.
    Parameters
    ----------
	None
    """
	required_climbers = 2
	gear_required = True

	def calculate_effort(self):
		effort = 3

		return effort + self.required_climbers

class Bouldering(Route):
	""" Child class that inherits from Route. Implements the calculate_effort() method.
    Parameters
    ----------
	None
    """
	required_climbers = 1
	gear_required = False
	
	def calculate_effort(self):
		# Very Convienient, low effort.
		return 0

class Lead(Route):
	"""Child class that inherits from Route. Implements the calculate_effort() method.
    Parameters
    ----------
	None
    """
	required_climbers = 2
	gear_required = True

	def calculate_effort(self):
		effort = 3

		return effort + self.required_climbers

