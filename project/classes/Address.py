#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Address(object):
	def getStreet(self):
		"""@ReturnType String"""
		return self.___street

	def setStreet(self, aStreet):
		"""@ParamType aStreet String
		@ReturnType void"""
		self.___street = aStreet

	def getCity(self):
		"""@ReturnType String"""
		return self.___city

	def setCity(self, aCity):
		"""@ParamType aCity String
		@ReturnType void"""
		self.___city = aCity

	def getState(self):
		"""@ReturnType String"""
		return self.___state

	def setState(self, aState):
		"""@ParamType aState String
		@ReturnType void"""
		self.___state = aState

	def getZipCode(self):
		"""@ReturnType String"""
		return self.___zipCode

	def setZipCode(self, aZipCode):
		"""@ParamType aZipCode String
		@ReturnType void"""
		self.___zipCode = aZipCode

	def __init__(self, street, city, state, zipCode):
		self.___street = street
		"""@AttributeType String"""
		self.___city = city
		"""@AttributeType String"""
		self.___state = state
		"""@AttributeType String"""
		self.___zipCode = zipCode
		"""@AttributeType String"""

