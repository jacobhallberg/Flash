class Address(object):
	""" Stateful class that holds address attributes.
	
	Parameters
	----------
	street (str): Street of user's address.
	city (str): City of user's address.
	state (str): State of user's address.
	zip_code (str): Zip Code of user's address.
	"""

	def get_street(self):
		return self.___street

	def get_city(self):
		return self.___city

	def get_state(self):
		return self.___state

	def get_zip_code(self):
		return self.___zip_code

	def __init__(self, street, city, state, zip_code):
		self.___street = street
		self.___city = city
		self.___state = state
		self.___zip_code = zip_code

