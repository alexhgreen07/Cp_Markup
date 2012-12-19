import sys
import os

#C+ class method storage
class Cp_Method:
	
	def __init__(self, init_name = ""):
		
		self.name = init_name
		self.parameters = {}
		self.return_value = ""
		self.is_static = False
		self.method_body = ""

#C+ class storage
class Cp_Class:
	
	def __init__(self, init_name = ""):
		
		self.name = init_name
		self.enums = {}
		self.structs = {}
		self.members = {}
		self.methods = {}

#C+ namespace storage
class Cp_Namespace:
	
	def __init__(self, init_name = ""):
		
		self.name = init_name
		self.classes = {}
		self.enums = {}
		self.structs = {}
		self.variables = {}
		self.functions = {}

#C+ import
class Cp_Import:
	
	def __init__(self, init_name = "", path = ""):
		
		self.name = init_name
		self.path = ""
		self.is_library = False
		
		self.namespaces = {}
		self.classes = {}
		self.enums = {}
		self.structs = {}
		self.variables = {}
		self.functions = {}

class Cp_Program:
	
	def __init__(self,init_name = ""):
		
		self.name = init_name
		
		self.imports = {}
		self.namespaces = {}
		self.classes = {}
		self.enums = {}
		self.structs = {}
		self.variables = {}
		self.functions = {}
