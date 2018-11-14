from classes.ContactInfo import ContactInfo

class ClimberInfo(ContactInfo):
	def getFirstname(self):
		return self.___firstname

	def setFirstname(self, aFirstname):
		self.___firstname = aFirstname

	def getLastname(self):
		return self.___lastname

	def getSkillLevel(self):
		return self.___skill_level

	def setLastname(self, aLastname):
		self.___lastname = aLastname
	
	def getContactInfo(self):
		return self.___contact_info

	def __init__(self, firstname, lastname, address, phone_number, skill_level):
		self.___firstname = firstname
		self.___lastname = lastname
		self.___contact_info = ContactInfo(address, phone_number)
		self.___skill_level = skill_level
		

