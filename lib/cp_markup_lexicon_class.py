import sys
import os
import time

import cp_markup_lexicon_global
from cp_markup_lexicon_global import *
import cp_markup_lexicon_struct_union
import cp_markup_lexicon_enum
import cp_markup_lexicon_function
import cp_markup_lexicon_variable

current_path, current_file = os.path.split(os.path.abspath(__file__))
sys.path.append(current_path + "/../plex-2.0.0dev/src")

import plex
from plex import *

bracket_counter = 0
brace_counter = 0
previous_state = ""

def Advance_To_Class_Name(scanner,text):
	
	print "Detected class name '%s'" % text
	
	scanner.begin("class_scope_state_parameters_start")

def Class_Definition_Start(scanner,text):
	
	global previous_state

	previous_state = scanner.state_name
	
	scanner.begin("class_scope_state_space_start")

def Advance_To_Class_Params_Name(scanner,text):
	
	print "Advancing to parameter list."
	
	global brace_counter
	brace_counter = 0
	
	scanner.begin("class_scope_state_parameters_name")

def Advance_To_Class_Scope(scanner,text):
	
	global bracket_counter
	
	print "In class scope."
	Class_Open_Bracket(scanner,text)
	
	bracket_counter = scanner.nesting_level
	
	scanner.begin("class_scope")
	
def Class_Open_Bracket(scanner,text):
	
	scanner.cp_open_bracket(text)

def Class_Close_Bracket(scanner,text):
	
	global previous_state
	global bracket_counter
	
	scanner.cp_close_bracket(text)
	
	if scanner.nesting_level < bracket_counter:
		
		print "Leaving class scope."
		
		scanner.begin(previous_state)

def Open_Brace(scanner,text):
	
	global brace_counter
	brace_counter = brace_counter + 1

def Close_Brace(scanner,text):
	
	global brace_counter
	brace_counter = brace_counter - 1
	
	if brace_counter < 0:
		
		print "Parameter list complete."
		
		scanner.begin("class_scope_bracket")

class_scope_state_parameters_name = State(
	"class_scope_state_parameters_name", [
		(whitespace_chars,   IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(valid_name_chars,"parameter strings"),
		(Str("*"),"parameter strings"),
		(Str("::"),"parameter strings"),
		(Str(","),"parameter separator"),
		(Str("("),Open_Brace),
		(Str(")"),Close_Brace)
	]
)

class_scope_state_parameters_start = State(
	"class_scope_state_parameters_start", [
		(whitespace_chars,   IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(Str("("), Advance_To_Class_Params_Name)
	]
)

class_scope_state_space = State(
	"class_scope_state_space_start", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(valid_name_chars,Advance_To_Class_Name)
	]
)

class_scope_bracket = State(
	"class_scope_bracket", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(Str("{"),Advance_To_Class_Scope)
	]
)

class_scope = State(
	"class_scope", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(c_bracket_open, Class_Open_Bracket),
		(c_bracket_closed, Class_Close_Bracket)
	] + \
	cp_markup_lexicon_struct_union.Get_Token_Tuples() + \
	cp_markup_lexicon_enum.Get_Token_Tuples() + \
	cp_markup_lexicon_function.Get_Token_Tuples() + \
	cp_markup_lexicon_variable.Get_Token_Tuples()
)

token_tuple = (Str("class") + force_whitespace, Class_Definition_Start)

lexicon_list_states = []
lexicon_list_states.append(class_scope_state_space)
lexicon_list_states.append(class_scope_state_parameters_start)
lexicon_list_states.append(class_scope_state_parameters_name)
lexicon_list_states.append(class_scope_bracket)
lexicon_list_states.append(class_scope)


#master lexicon list
lexicon_list = []

lexicon_list = lexicon_list + lexicon_list_states

def Get_Token_Tuples():
	
	return [token_tuple]

def Get_Lexicon_List():
	
	return lexicon_list

		
