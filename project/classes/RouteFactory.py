from abc import ABC, abstractmethod
from classes import Route
from enum import Enum

class BoulderingTypes(Enum):
    bouldering = "Boulder"
    lead = "Lead"
    topRope = "TopRope"

class AbstractRouteFactory(ABC):
    @abstractmethod
    def createBoulderingRoute(self):
        pass

    @abstractmethod
    def createTopRopeRoute(self):
        pass

    @abstractmethod
    def createLeadRoute(self):
        pass

class RouteFactory(AbstractRouteFactory):
    def createBoulderingRoute(self, name, location, holds, actualDifficulty, feltDifficulty):
        return Route.Bouldering(name, location, holds, actualDifficulty, feltDifficulty)
    
    def createLeadRoute(self, name, location, holds, actualDifficulty, feltDifficulty):
        return Route.Lead(name, location, holds, actualDifficulty, feltDifficulty)
    
    def createTopRopeRoute(self, name, location, holds, actualDifficulty, feltDifficulty):
        return Route.TopRope(name, location, holds, actualDifficulty, feltDifficulty)

    @staticmethod
    def createRoute(self, routeType, name, location, holds, actualDifficulty, feltDifficulty):
        if routeType == BoulderingTypes.bouldering.value:
            return self.createBoulderingRoute(name, location, holds, actualDifficulty, feltDifficulty)
        elif routeType == BoulderingTypes.lead.value:
            return self.createLeadRoute(name, location, holds, actualDifficulty, feltDifficulty)
        elif routeType == BoulderingTypes.topRope.value:
            return self.createTopRopeRoute(name, location, holds, actualDifficulty, feltDifficulty)
        else:
            return -1

