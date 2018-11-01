#!/usr/bin/python
# -*- coding: UTF-8 -*-
from classes.ContactInfo import ContactInfo

class ClimberInfo(ContactInfo):
	def getFirstname(self):
		"""@ReturnType String"""
		return self.___firstname

	def setFirstname(self, aFirstname):
		"""@ParamType aFirstname String
		@ReturnType void"""
		self.___firstname = aFirstname

	def getLastname(self):
		"""@ReturnType String"""
		return self.___lastname

	def setLastname(self, aLastname):
		"""@ParamType aLastname String
		@ReturnType void"""
		self.___lastname = aLastname
	
	def getContactInfo(self):
		return self.___contact_info

	def __init__(self, firstname, lastname, address, phone_number):
		self.___firstname = firstname
		"""@AttributeType String"""
		self.___lastname = lastname
		"""@AttributeType String"""
		self.___contact_info= ContactInfo(address, phone_number)
		

