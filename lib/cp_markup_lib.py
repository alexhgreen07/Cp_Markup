import sys
import os
import time

import cp_markup_lexicon_global
from cp_markup_lexicon_global import *

import cp_markup_lexicon_class
import cp_markup_lexicon_namespace
import cp_markup_lexicon_import
import cp_markup_lexicon_using
import cp_markup_lexicon_struct_union
import cp_markup_lexicon_enum
import cp_markup_lexicon_function
import cp_markup_lexicon_variable

import cp_language_objects
from cp_language_objects import *

current_path, current_file = os.path.split(os.path.abspath(__file__))
sys.path.append(current_path + "/../plex-2.0.0dev/src")

import plex
from plex import *

time_start = time.time()

class CpScanner(Scanner):

	#open bracket
	def cp_open_bracket(self,text):
		
		self.nesting_level = self.nesting_level + 1
		
		print "Open bracket. Nesting level at '%d'" % self.nesting_level
	
	#close bracket
	def cp_close_bracket(self,text):
	
		self.nesting_level = self.nesting_level - 1
		
		print "Closed bracket. Nesting level at '%d'" % self.nesting_level
		
		if self.nesting_level < 0:
			
			raise Exception("Unknown bracket format.")

	def cp_open_comment(self,text):
		
		print "C open comment '%s'" % text
		
		self.last_state = self.state_name
		
		self.begin("comment_open")
		
	def cp_close_comment(self,text):
	
		print "C close comment '%s'" % text
		
		self.begin(self.last_state)
	
	#master lexicon list
	lexicon_list = []

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
	
	
	def __init__(self,filehandle,name):
	
		Scanner.__init__(self,self.lexicon,filehandle,name)
		
		#define parsing variables
		self.nesting_level = 0
		self.last_state = ""
		
		#define the object lists
		self.import_file_list = []
		self.namespace_dictionary = {}
		self.class_dictionary = {}
		
		#define the current scope variables
		self.using_namespace_dictionary = {}
		self.current_namespace_scope = ""
		self.current_class_scope = ""
		
		
