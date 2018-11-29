class ContactInfo:
	""" Info class that takes in 
		address and phone number as parameters.
    Parameters
    ----------
	address (Address): Address object holding user's address information.
	phone_number (str): The user's phone number.
    """
	def get_address(self):
		return self.___address

	def get_phone_number(self):
		return self.___phone_number

	def __init__(self, address, phone_number):
		self.___address = address
		self.___phone_number = phone_number

