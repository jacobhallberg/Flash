class Climber(object):
	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.___username

	def getUsername(self):
		return self.___username

	def getFavoriteGym(self):
		return self.___favoriteGym

	def setFavoriteGym(self, aFavoriteGym):
		self.___favoriteGym = aFavoriteGym

	def getInfo(self):
		return self.___info

	def setInfo(self, aInfo):
		self.___info = aInfo

	def getRoutes(self):
		return self.___routes

	def __init__(self, username, password, favoriteGym = None, info = None, routes = None):
		self.___username = username
		self.___password = password
		self.___favoriteGym = favoriteGym
		self.___info = info
		self.___routes = routes

