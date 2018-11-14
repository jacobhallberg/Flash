from abc import ABC, abstractclassmethod
from classes.Workout import Workout
from classes.RouteFactory import RouteFactory
import heapq


class WorkoutStrategy(ABC):
    fields = ["Type", "Holds", "Actual Difficulty"]

    def make_route(self, route):
        return RouteFactory.createRoute(RouteFactory(), route["routeType"], route["routeName"], route["location"], route["holds"], route["actualDifficulty"], route["feltDifficulty"])

    @abstractclassmethod
    def similarity_score(self, target_difficulty, true_difficulty):
        pass

    @abstractclassmethod
    def algorithm_interface(self, routes, workout_info):
        pass


class BeginnerWorkout(WorkoutStrategy):
    target_difficulty = 3

    def similarity_score(self, route_difficulty):
        if int(route_difficulty) <= self.target_difficulty + .5:
            return 10
        else:
            return 0

    def algorithm_interface(self, routes, workout_info):
        route_scores = []
        route_dict = {}

        for route in routes:
            route_score = 0
            route = self.make_route(route)

            if route.getHolds() in workout_info.holds.data:
                route_score += 1
            if route.__class__.__name__ in workout_info.types.data:
                route_score += 2

            route_dict[route.getName()] = route
            route_score += self.similarity_score(route.getActualDifficulty())
            route_score += route.calculateEffort()

            heapq.heappush(route_scores, (route_score, route.getName()))

        selected_routes = heapq.nlargest(workout_info.numRoutes.data, route_scores)
        return [route_dict[name] for _, name in selected_routes]


class IntermediateWorkout(WorkoutStrategy):
    target_difficulty = 4

    def similarity_score(self, route_difficulty):
        max_score = 5
        return (max_score + self.target_difficulty - int(route_difficulty)) * 3

    def algorithm_interface(self, routes, workout_info):
        route_scores = []
        route_dict = {}

        for route in routes:
            route_score = 0
            route = self.make_route(route)

            if route.getHolds() in workout_info.holds.data:
                route_score += 3
            if route.__class__.__name__ in workout_info.types.data:
                route_score += 5

            route_dict[route.getName()] = route
            route_score += self.similarity_score(route.getActualDifficulty())
            route_score += route.calculateEffort()
            
            heapq.heappush(route_scores, (route_score, route.getName()))

        selected_routes = heapq.nlargest(workout_info.numRoutes.data, route_scores)
        return [route_dict[name] for _, name in selected_routes]


class AdvancedWorkout(WorkoutStrategy):
    target_difficulty = 5

    def similarity_score(self, route_difficulty):
        max_score = 5
        return (max_score + self.target_difficulty - int(route_difficulty)) * 2

    def algorithm_interface(self, routes, workout_info):
        route_scores = []
        route_dict = {}

        for route in routes:
            route_score = 0
            route = self.make_route(route)

            if route.getHolds() in workout_info.holds.data:
                route_score += 7
            if route.__class__.__name__ in workout_info.types.data:
                route_score += 9

            route_dict[route.getName()] = route
            route_score += self.similarity_score(route.getActualDifficulty())
            route_score += route.calculateEffort()
            
            heapq.heappush(route_scores, (route_score, route.getName()))

        selected_routes = heapq.nlargest(workout_info.numRoutes.data, route_scores)
        return [route_dict[name] for _, name in selected_routes]
