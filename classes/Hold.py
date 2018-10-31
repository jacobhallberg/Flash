#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Hold(object):
	def getHoldType(self):
		"""@ReturnType String"""
		return self.___holdType

	def setHoldType(self, aHoldType):
		"""@ParamType aHoldType String
		@ReturnType void"""
		self.___holdType = aHoldType

	def getHoldDifficulty(self):
		"""@ReturnType Integer"""
		return self.___holdDifficulty

	def setHoldDifficulty(self, aHoldDifficulty):
		"""@ParamType aHoldDifficulty Integer
		@ReturnType void"""
		self.___holdDifficulty = aHoldDifficulty

	def __init__(self, holdType, holdDifficulty):
		self.___holdType = holdType
		"""@AttributeType String"""
		self.___holdDifficulty = holdDifficulty
		"""@AttributeType Integer"""
