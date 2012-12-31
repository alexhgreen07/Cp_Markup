## @package cp_markup_scanner
# @brief This file contains the Plex C+ scanner class used for parsing the 
# C+ code files.

import sys
import os
import time

#import the global lexicon library
import cp_markup_lexicon_global
from cp_markup_lexicon_global import *

#import the individual language lexicon library elements
import cp_markup_lexicon_class
import cp_markup_lexicon_namespace
import cp_markup_lexicon_import
import cp_markup_lexicon_using
import cp_markup_lexicon_struct_union
import cp_markup_lexicon_enum
import cp_markup_lexicon_function
import cp_markup_lexicon_variable

#import the storage objects for the C+ elements
import cp_markup_language_objects
from cp_markup_language_objects import *

current_path, current_file = os.path.split(os.path.abspath(__file__))
sys.path.append(current_path + "/plex-2.0.0dev/src")

#import the plex parsing library
import plex
from plex import *

time_start = time.time()

## @brief This is the class for the C+ scanner.	
# It inherits from the Plex scanner class.
class CpScanner(Scanner):

	## @brief This functions should be called anytime an open 
	# bracket '{' is contained in the C+ markup.
	# @param text This is the text which triggered the function callback.
	def cp_open_bracket(self,text):

		
		self.nesting_level = self.nesting_level + 1
		
		print "Open bracket. Nesting level at '%d'" % self.nesting_level
	
	## @brief This functions should be called anytime an closed 
	# bracket '}' is contained in the C+ markup.
	def cp_close_bracket(self,text):
	
		self.nesting_level = self.nesting_level - 1
		
		print "Closed bracket. Nesting level at '%d'" % self.nesting_level
		
		if self.nesting_level < 0:
			
			raise Exception("Unknown bracket format.")

	## @brief This functions should be called anytime an open 
	# comment delimiter '/*' is contained in the C+ markup.
	def cp_open_comment(self,text):
		
		print "C open comment '%s'" % text
		
		self.last_state = self.state_name
		
		self.begin("comment_open")
	
	## @brief This functions should be called anytime an closed 
	# comment delimiter '*/' is contained in the C+ markup.
	def cp_close_comment(self,text):
	
		print "C close comment '%s'" % text
		
		self.begin(self.last_state)
	
	#master lexicon list
	lexicon_list = []

	#global tokens
	lexicon_list.append((whitespace_chars,   IGNORE))
	lexicon_list.append((c_comments,"comment"))
	lexicon_list.append((preprocessor,"preprocessor"))
	lexicon_list.append((c_bracket_open, cp_open_bracket))
	lexicon_list.append((c_bracket_closed, cp_close_bracket))
	
	#load all tokens for valid global declarations
	lexicon_list = lexicon_list + cp_markup_lexicon_class.Get_Token_Tuples()
	lexicon_list = lexicon_list + cp_markup_lexicon_namespace.Get_Token_Tuples()
	lexicon_list = lexicon_list + cp_markup_lexicon_import.Get_Token_Tuples()
	lexicon_list = lexicon_list + cp_markup_lexicon_using.Get_Token_Tuples()
	lexicon_list = lexicon_list + cp_markup_lexicon_struct_union.Get_Token_Tuples()
	lexicon_list = lexicon_list + cp_markup_lexicon_enum.Get_Token_Tuples()
	lexicon_list = lexicon_list + cp_markup_lexicon_function.Get_Token_Tuples()
	lexicon_list = lexicon_list + cp_markup_lexicon_variable.Get_Token_Tuples()
	
	#load all states from all lexicon lists
	lexicon_list = lexicon_list + cp_markup_lexicon_class.Get_Lexicon_List()
	lexicon_list = lexicon_list + cp_markup_lexicon_namespace.Get_Lexicon_List()
	lexicon_list = lexicon_list + cp_markup_lexicon_import.Get_Lexicon_List()
	lexicon_list = lexicon_list + cp_markup_lexicon_using.Get_Lexicon_List()
	lexicon_list = lexicon_list + cp_markup_lexicon_struct_union.Get_Lexicon_List()
	lexicon_list = lexicon_list + cp_markup_lexicon_enum.Get_Lexicon_List()
	lexicon_list = lexicon_list + cp_markup_lexicon_function.Get_Lexicon_List()
	lexicon_list = lexicon_list + cp_markup_lexicon_variable.Get_Lexicon_List()
	
	#initialize lexicon object
	lexicon = Lexicon(lexicon_list)
	
	## @brief This is the initializer function for the class.
	def __init__(self,filehandle,name):
		
		Scanner.__init__(self,self.lexicon,filehandle,name)
		
		#define parsing variables
		self.nesting_level = 0
		self.last_state = ""
		
		#define the object lists
		self.import_file_list = []
		self.current_cp_file = Cp_File(name)
		
		#define the current scope variables
		self.using_namespace_dictionary = {}
		self.current_namespace_scope = ""
		self.current_class_scope = ""
		
		
