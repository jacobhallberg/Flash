class Address(object):
	def getStreet(self):
		return self.___street

	def setStreet(self, aStreet):
		self.___street = aStreet

	def getCity(self):
		return self.___city

	def setCity(self, aCity):
		self.___city = aCity

	def getState(self):
		return self.___state

	def setState(self, aState):
		self.___state = aState

	def getZipCode(self):
		return self.___zipCode

	def setZipCode(self, aZipCode):
		self.___zipCode = aZipCode

	def __init__(self, street, city, state, zipCode):
		self.___street = street
		self.___city = city
		self.___state = state
		self.___zipCode = zipCode

