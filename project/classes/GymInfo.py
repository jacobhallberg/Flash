#!/usr/bin/python
# -*- coding: UTF-8 -*-
from ContactInfo import ContactInfo

class GymInfo(ContactInfo):
	def getHoursOfOperation(self):
		"""@ReturnType String"""
		return self.___hoursOfOperation

	def setHoursOfOperation(self, aHoursOfOperation):
		"""@ParamType aHoursOfOperation String
		@ReturnType void"""
		self.___hoursOfOperation = aHoursOfOperation

	def __init__(self, hoursOfOperation):
		self.___hoursOfOperation = hoursOfOperation
		"""@AttributeType String"""
