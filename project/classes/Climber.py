from abc import ABC, abstractclassmethod

class User:
	""" Abstract class used to make Flask's login library work with 
		climber class objects by adding required methods to the child class.
    Parameters
    ----------
	None
    """
	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	@abstractclassmethod
	def get_id(self):
		pass

class Climber(User):
	""" The climber class holds all of a user's information. 
    Parameters
    ----------
	username (str): Unique string denoting user's username.
	info (ClimberInfo): Object holding personal information about the user.
	routes (list<Route>): List of route objects created by the user.
    """
	def get_id(self):
		return self.___username

	def get_username(self):
		return self.___username

	def get_info(self):
		return self.___info

	def get_routes(self):
		return self.___routes

	def __init__(self, username, info = None, routes = None):
		self.___username = username
		self.___info = info
		self.___routes = routes

