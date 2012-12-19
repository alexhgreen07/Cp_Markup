import sys
import os
import time

import cp_markup_lexicon_global
from cp_markup_lexicon_global import *

current_path, current_file = os.path.split(os.path.abspath(__file__))
sys.path.append(current_path + "/../plex-2.0.0dev/src")

import plex
from plex import *

brace_counter = 0
previous_state = ""

def Advance_To_Variable_Name(scanner,text):
	
	print "Detected variable name '%s'" % text
	
	scanner.begin("variable_scope_state_parameters_start")

def Advance_To_Variable_Params(scanner,text):
	
	print "Advancing to parameter list"
	
	scanner.begin("variable_scope_state_parameters_start")

def Variable_Definition_Start(scanner,text):
	
	print "Variable found: '%s'" % text
	
	#previous_state = scanner.state_name
	
	#scanner.begin("variable_scope_state_space_start")

def Advance_To_Variable_Params_Name(scanner,text):
	
	print "Advancing to parameter list."
	
	global brace_counter
	brace_counter = 0
	
	scanner.begin("variable_scope_state_parameters_name")

def Open_Brace(scanner,text):
	
	global brace_counter
	brace_counter = brace_counter + 1

def Close_Brace(scanner,text):
	
	global brace_counter
	brace_counter = brace_counter - 1
	
	if brace_counter < 0:
		
		print "Parameter list complete."
		
		global previous_state
		
		scanner.begin(previous_state)

variable_scope_state_parameters_name = State(
	"variable_scope_state_parameters_name", [
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

variable_scope_state_parameters_start = State(
	"variable_scope_state_parameters_start", [
		(whitespace_chars,   IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(Str("("), Advance_To_Variable_Params_Name)
	]
)

variable_scope_state_space = State(
	"variable_scope_state_space_start", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(valid_name_chars,Advance_To_Variable_Name)
	]
)

#<type> <modifier list> <name> ([<size>]) (= <value>);
variable_search_pattern = Str("public","private") + force_whitespace + valid_name_chars + Opt(Rep(force_whitespace + valid_name_chars)) + whitespace + Opt(Rep(Str("*"))) +  force_whitespace + valid_name_chars + whitespace + Opt(Str("[") + Rep(AnyBut("]")) + Str("]") + whitespace) + Opt(Str("=") + Rep(AnyBut(";"))) + Str(";")

token_tuple = (variable_search_pattern, Variable_Definition_Start)

lexicon_list_states = []
lexicon_list_states.append(variable_scope_state_space)
lexicon_list_states.append(variable_scope_state_parameters_start)
lexicon_list_states.append(variable_scope_state_parameters_name)


#master lexicon list
lexicon_list = []

lexicon_list = lexicon_list + lexicon_list_states

def Get_Token_Tuples():
	
	return [token_tuple]

def Get_Lexicon_List():
	
	return lexicon_list

		
