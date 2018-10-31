#!/usr/bin/python
# -*- coding: UTF-8 -*-

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
		"""@ReturnType String"""
		return self.___username

	def getFavoriteGym(self):
		"""@ReturnType Gym"""
		return self.___favoriteGym

	def setFavoriteGym(self, aFavoriteGym):
		"""@ParamType aFavoriteGym Gym
		@ReturnType void"""
		self.___favoriteGym = aFavoriteGym

	def getInfo(self):
		"""@ReturnType ClimberInfo"""
		return self.___info

	def setInfo(self, aInfo):
		"""@ParamType aInfo ClimberInfo
		@ReturnType void"""
		self.___info = aInfo

	def getRoutes(self):
		return self.___routes

	def __init__(self, username, password, favoriteGym = None, info = None, routes = None):
		self.___username = username
		"""@AttributeType String"""
		self.___password = password
		"""@AttributeType String"""
		self.___favoriteGym = favoriteGym
		"""@AttributeType GymInfo"""
		self.___info = info
		"""@AttributeType ClimberInfo"""
		self.___routes = routes
		"""@AttributeType ArrayList"""

