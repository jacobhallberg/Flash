from abc import ABC, abstractclassmethod

class Hold(ABC):
	""" Abstract class used in the decorator design pattern. Forces children to
		take in hold_type as a parameter.
    Parameters
    ----------
	hold_type (str): String denoting the type of holds selected from the HoltTypes enum.
    """
	def __init__(self, hold_type):
		self.hold_type = hold_type

	@abstractclassmethod
	def return_holds(self):
		pass

class BaseHold(Hold):
	""" Concrete class used in the decorator design pattern. Implements return holds
		and doesn't recursively class decorators because its of BaseHold type.
    Parameters
    ----------
	None
    """
	def return_holds(self):
		return [self.hold_type]

class Decorator(Hold, ABC):
	""" Abstract class used in the decorator design pattern. Forces children to
		take in hold_types and component, as well as implement return holds.
    Parameters
    ----------
	hold_type (str): String denoting the type of holds selected from the HoltTypes enum.
	component (BaseHold | DecoratorHold): 
    """
	def __init__(self, hold_type, component):
		self.hold_type = hold_type
		self.component = component

	@abstractclassmethod
	def return_holds(self):
		""" Returns list of hold types.
		"""
		pass
 
class DecoratorHold(Decorator):
	""" Concrete hold class used in the decorator design pattern. Builds up a list
		recursively by calling return_holds on the component object.
    Parameters
    ----------
	None
    """
	def return_holds(self):
		""" Returns list of hold types.
		"""
		return self.component.return_holds() + [self.hold_type] 
