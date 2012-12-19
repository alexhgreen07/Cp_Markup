import sys
import os

#C+ class method storage
class Cp_Method:
	
	def __init__(self, init_name = ""):
		
		self.name = init_name
		self.parameters = []
		self.return_value = ""
		self.is_static = False

#C+ class storage
class Cp_Class:
	
	def __init__(self, init_name = ""):
		
		self.name = init_name
		self.enums = []
		self.structs = []
		self.members = []
		self.methods = []

#C+ namespace storage
class Cp_Namespace:
	
	def __init__(self, init_name = ""):
		
		self.name = init_name
		self.classes = []
		self.enums = []
		self.structs = []
		self.variables = []
		self.functions = []
