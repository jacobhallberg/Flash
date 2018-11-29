from classes.ContactInfo import ContactInfo

class ClimberInfo():
	""" Stores personal information about a user.
    Parameters
    ----------
	firstname (str): The user's firstname.
	lastname (str): The user's lastname.
	address (Address): Address object holding user's address information.
	phone_number (str): The user's phone number.
	skill_level (str): The user's climbing skill level chosen from 
						the SkillLevels enum.
    """
	def get_firstname(self):
		return self.___firstname

	def get_lastname(self):
		return self.___lastname

	def get_skill_level(self):
		return self.___skill_level

	def get_contact_info(self):
		return self.___contact_info

	def __init__(self, firstname, lastname, address, phone_number, skill_level):
		self.___firstname = firstname
		self.___lastname = lastname
		self.___contact_info = ContactInfo(address, phone_number)
		self.___skill_level = skill_level
		

