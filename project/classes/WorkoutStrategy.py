from abc import ABC, abstractclassmethod
from classes.Workout import Workout
from classes.RouteFactory import RouteFactory
import heapq
from math import floor

class WorkoutStrategy(ABC):
    """ Abstract class, that uses different similarity score algorithms depending on the skill level 
        of the climber. Forces children to implement similarity_score().
    Parameters
    ----------
    None
    """

    @abstractclassmethod
    def similarity_score(self, route_difficulty):
        pass

    def make_route(self, route):
        return RouteFactory.create_route(RouteFactory(), route["route_type"], route["route_name"], route["location"], route["holds"], route["actual_difficulty"], route["felt_difficulty"])

    def generate_routes(self, routes, workout_info):
        route_scores = []
        route_dict = {}

        for route in routes:
            route_score = 0
            route = self.make_route(route)

            if route.__class__.__name__ in workout_info.types.data:     
                if route.get_holds() in workout_info.holds.data:
                    route_score += 1

                route_dict[route.get_name()] = route
                route_score += self.similarity_score(route.get_actual_difficulty())
                route_score -= route.calculate_effort()

                heapq.heappush(route_scores, (route_score, route.get_name()))

        selected_routes = heapq.nlargest(floor(workout_info.numRoutes.data), route_scores)

        return [route_dict[name] for _, name in selected_routes]

class BeginnerWorkout(WorkoutStrategy):
    """ Inherits from WorkoutStrategy and implements similarity_score().
    Parameters
    ----------
    None
    """
    target_difficulty = 3.5

    def similarity_score(self, route_difficulty):
        if float(route_difficulty) <= self.target_difficulty:
            return 10
        else:
            return 0

class IntermediateWorkout(WorkoutStrategy):
    """ Inherits from WorkoutStrategy and implements similarity_score().
    Parameters
    ----------

    """
    target_difficulty = 4

    def similarity_score(self, route_difficulty):
        max_score = 5
        return (max_score + self.target_difficulty - int(route_difficulty)) * 3

class AdvancedWorkout(WorkoutStrategy):
    """ Inherits from WorkoutStrategy and implements similarity_score().
    Parameters
    ----------

    """
    target_difficulty = 5

    def similarity_score(self, route_difficulty):
        max_score = 5
        return (max_score + self.target_difficulty - int(route_difficulty)) * 2
