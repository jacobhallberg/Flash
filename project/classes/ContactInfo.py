from abc import ABC

class ContactInfo(ABC):
	def getAddress(self):
		return self.___address

	def setAddress(self, aAddress):
		self.___address = aAddress

	def getPhoneNumber(self):
		return self.___phoneNumber

	def setPhoneNumber(self, aPhoneNumber):
		self.___phoneNumber = aPhoneNumber

	def __init__(self, address, phoneNumber):
		self.___address = address
		self.___phoneNumber = phoneNumber

