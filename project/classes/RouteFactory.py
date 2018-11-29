from abc import ABC, abstractclassmethod
from enum import Enum
from classes import Route


class ClimbingTypes(Enum):
    """ Enum defining the three climbing types available.

    """

    bouldering = "Bouldering"
    lead = "Lead"
    topRope = "TopRope"


class AbstractRouteFactory(ABC):
    """ Abstract class defining methods to be implemented for the factory design pattern.
    
    Parameters
    ----------
    None
    """
    @abstractclassmethod
    def create_bouldering_route(self):
        pass

    @abstractclassmethod
    def create_top_rope_route(self):
        pass

    @abstractclassmethod
    def create_lead_route(self):
        pass

class RouteFactory(AbstractRouteFactory):
    """Concrete class that implements the factory design pattern by inheriting from the
         AbstractRouteFactory class. Given a type from the ClimbingTypes enum, returns 
         the created route object.
    Parameters
    ----------
    route_type (ClimbingTypes):
	name (str): The nane of the route.
	location (str): The location of the route.
	holds (Hold): Hold object with each hold found on the route.
	actual_difficulty (int): The rating given by the gym.
	felt_difficulty (int): The rating that the climber gives to the route.
    """
    def create_bouldering_route(self, name, location, holds, actual_difficulty, felt_difficulty):
        return Route.Bouldering(name, location, holds, actual_difficulty, felt_difficulty)
    
    def create_lead_route(self, name, location, holds, actual_difficulty, felt_difficulty):
        return Route.Lead(name, location, holds, actual_difficulty, felt_difficulty)
    
    def create_top_rope_route(self, name, location, holds, actual_difficulty, felt_difficulty):
        return Route.TopRope(name, location, holds, actual_difficulty, felt_difficulty)

    @staticmethod
    def create_route(self, route_type, name, location, holds, actual_difficulty, felt_difficulty):
        if route_type == ClimbingTypes.bouldering.value:
            return self.create_bouldering_route(name, location, holds, actual_difficulty, felt_difficulty)
        elif route_type == ClimbingTypes.lead.value:
            return self.create_lead_route(name, location, holds, actual_difficulty, felt_difficulty)
        elif route_type == ClimbingTypes.topRope.value:
            return self.create_top_rope_route(name, location, holds, actual_difficulty, felt_difficulty)
        else:
            return -1
