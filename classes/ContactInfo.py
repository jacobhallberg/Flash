#!/usr/bin/python
# -*- coding: UTF-8 -*-
from abc import ABC

class ContactInfo(ABC):
	def getAddress(self):
		"""@ReturnType Address"""
		return self.___address

	def setAddress(self, aAddress):
		"""@ParamType aAddress Address
		@ReturnType void"""
		self.___address = aAddress

	def getPhoneNumber(self):
		"""@ReturnType String"""
		return self.___phoneNumber

	def setPhoneNumber(self, aPhoneNumber):
		"""@ParamType aPhoneNumber String
		@ReturnType void"""
		self.___phoneNumber = aPhoneNumber

	def __init__(self, address, phoneNumber):
		self.___address = address
		"""@AttributeType Address"""
		self.___phoneNumber = phoneNumber
		"""@AttributeType String"""

