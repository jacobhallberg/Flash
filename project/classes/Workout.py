class Workout(object):
	def getRoutes(self):
		return self.___routes

	def getName(self):
		return self.___name

	def __init__(self, routes, requested_workout_info, workout_algorithm):
		self.___routes = workout_algorithm.algorithm_interface(routes, requested_workout_info)
		self.___name = requested_workout_info["name"].data
