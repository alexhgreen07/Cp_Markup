## @package cp_markup_lexicon_namespace
# @brief This file contains all lexical objects and functions for parsing
# C+ namespaces.

import sys
import os
import time

import cp_markup_lexicon_global
from cp_markup_lexicon_global import *
import cp_markup_lexicon_class
import cp_markup_lexicon_struct_union
import cp_markup_lexicon_enum
import cp_markup_lexicon_function
import cp_markup_lexicon_variable

#import the storage objects for the C+ elements
import cp_markup_language_objects
from cp_markup_language_objects import *

current_path, current_file = os.path.split(os.path.abspath(__file__))
sys.path.append(current_path + "/plex-2.0.0dev/src")

import plex
from plex import *

bracket_counter = 0
brace_counter = 0
previous_state = ""

## @brief This function begins the parsing of the namespace text
def Namespace_Definition_Start(scanner,text):
	
	previous_state = scanner.state_name
	
	scanner.begin("namespace_scope_state_space_start")

## @brief This function detects the namespace name string.
def Advance_To_Namespace_Name(scanner,text):
	
	#strip all whitespace by replacing with empty strings
	text = text.replace(" ","")
	text = text.replace("\t","")
	text = text.replace("\n","")
	text = text.replace("\r","")
	
	#parse the nested namespaces using the appropriate delimiter
	nested_namespace_list = text.rsplit("::")
	
	#store the highest level namespace
	parent_namespace = Cp_Namespace(nested_namespace_list.pop(0))
	
	#assign the namespace to the current file
	scanner.current_cp_file.namespaces[parent_namespace.name] = parent_namespace
	
	print "Parent namespace '%s' detected." % parent_namespace.name
	
	#store all child namespaces
	for nested_namespace in nested_namespace_list:
			
			#fill the new namespace with the appropriate data.
			new_namespace = Cp_Namespace(nested_namespace)
			
			print "Child namespace '%s' of '%s' detected." % (new_namespace.name,parent_namespace.name)
			
			#assign the namespace to the current file
			parent_namespace.namespaces[new_namespace.name] = new_namespace
			
	
	scanner.begin("namespace_scope_state_bracket")

## @brief This function is triggered when the open bracket is 
# detected after the namespace declaration.
def Advance_To_Namespace_Scope(scanner,text):
	
	global bracket_counter
	
	Namespace_Open_Bracket(scanner,text)
	bracket_counter = scanner.nesting_level
	
	print "In namespace scope at nesting level %d" % scanner.nesting_level
	
	scanner.begin("namespace_scope")

## @brief This function is called when an open bracket is detected.
def Namespace_Open_Bracket(scanner,text):
	
	scanner.cp_open_bracket(text)

## @brief This function is called when a closed bracket is detected.
def Namespace_Close_Bracket(scanner,text):
	
	global bracket_counter
	
	scanner.cp_close_bracket(text)
	
	if scanner.nesting_level < bracket_counter:
		
		print "Leaving namespace scope."
		
		scanner.begin(previous_state)
	
## @brief This is a Plex state object for detecting the namespace name text
namespace_scope_state_space = State(
	"namespace_scope_state_space_start", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(valid_name_chars + Opt(Rep(whitespace + Str("::") + whitespace + valid_name_chars)),Advance_To_Namespace_Name)
	]
)

## @brief This is a Plex state object for detecting the starting open bracket of the namespace scope.
namespace_scope_state_bracket = State(
	"namespace_scope_state_bracket", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(Str("{"),Advance_To_Namespace_Scope)
	]
)

## @brief This is a Plex state object for valid tokens within a namespace scope.
namespace_scope = State(
	"namespace_scope", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(c_bracket_open, Namespace_Open_Bracket),
		(c_bracket_closed, Namespace_Close_Bracket)
	] + \
	cp_markup_lexicon_class.Get_Token_Tuples() + \
	cp_markup_lexicon_struct_union.Get_Token_Tuples() + \
	cp_markup_lexicon_enum.Get_Token_Tuples() + \
	cp_markup_lexicon_function.Get_Token_Tuples() + \
	cp_markup_lexicon_variable.Get_Token_Tuples()
)

## @brief This is the token for detecting the start of a namespace definition.
token_tuple = (Str("namespace") + force_whitespace, Namespace_Definition_Start)

## @brief These are all states used for parsing namespaces
lexicon_list_states = []
lexicon_list_states.append(namespace_scope_state_space)
lexicon_list_states.append(namespace_scope_state_bracket)
lexicon_list_states.append(namespace_scope)


## @brief This is the master lexicon list for namespaces
lexicon_list = []
lexicon_list = lexicon_list + lexicon_list_states

def Get_Token_Tuples():
	
	return [token_tuple]

def Get_Lexicon_List():
	
	return lexicon_list

		
