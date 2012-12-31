## @package cp_markup_language_objects
# @brief This file contains all objects to store the 
# parsed language objects in.

import sys
import os

## @brief This stores the C+ method/function data and identifiers.
class Cp_Method:
	
	def __init__(self, init_name = ""):
		
		self.name = init_name
		self.parameters = {}
		self.return_value = ""
		self.is_static = False
		self.method_body = ""

## @brief This stores the C+ class data and identifiers.
class Cp_Class:
	
	def __init__(self, init_name = ""):
		
		self.name = init_name
		self.enums = {}
		self.structs = {}
		self.members = {}
		self.methods = {}

## @brief This stores the C+ namespace data and identifiers.
class Cp_Namespace:
	
	def __init__(self, init_name = ""):
		
		self.name = init_name
		self.namespaces = {}
		self.classes = {}
		self.enums = {}
		self.structs = {}
		self.variables = {}
		self.functions = {}

## @brief This stores the C+ file data and identifiers.
class Cp_File:
	
	def __init__(self, init_name = "", path = ""):
		
		## @brief This is a string containing the filename.
		self.name = init_name
		## @brief This is a string containing the file path.
		self.path = ""
		## @brief This is a boolean value of whether this is a library file or not. (Unused at the moment)
		self.is_library = False
		
		## @brief This list stores the names of the namespaces being used (including delimiters)
		self.using_names = []
		## @brief This is a dictionary of Cp_Namespace objects in the file. The key is the namespace name.
		self.namespaces = {}
		## @brief This is a dictionary of Cp_Class objects define in the file. The key is the class name.
		self.classes = {}
		## @brief This is a dictionary of Cp_Method objects in the file. The key is the method name.
		self.functions = {}
		
		self.enums = {}
		self.structs = {}
		self.variables = {}

## @brief This stores the C+ prorgram data and identifiers.
class Cp_Program:
	
	def __init__(self,init_name = ""):
		
		self.name = init_name
		
		## @brief This is a dictionary of Cp_File objects in the program. The key is the filename.
		self.files = {}
		## @brief This is a dictionary of Cp_Namespace objects in the program. The key is the namespace name.
		self.namespaces = {}
		## @brief This is a dictionary of Cp_Class objects in the program. The key is the class name.
		self.classes = {}
		## @brief This is a dictionary of Cp_Method objects in the program. The key is the function/method name.
		self.functions = {}
		
		self.enums = {}
		self.structs = {}
		self.variables = {}
