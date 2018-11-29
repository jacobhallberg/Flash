class Workout(object):
	""" Stores all the information regarding to a workout.
    Parameters
    ----------
	routes (list<Route>): List of routes that matched a climber's preference.
	requested_workout_info (dict): Object containing all of the climber's workout preferences.
	workout_algorithm (WorkoutStrategy): Workout algorithm determed by the strategy design pattern.
    """
	def get_routes(self):
		return self.___routes

	def get_name(self):
		return self.___name

	def __init__(self, routes, requested_workout_info, workout_algorithm):
		self.___routes = workout_algorithm.generate_routes(routes, requested_workout_info)
		self.___name = requested_workout_info["name"].data
