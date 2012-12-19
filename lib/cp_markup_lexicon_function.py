import sys
import os
import time

import cp_markup_lexicon_global
from cp_markup_lexicon_global import *

current_path, current_file = os.path.split(os.path.abspath(__file__))
sys.path.append(current_path + "/../plex-2.0.0dev/src")

import plex
from plex import *

bracket_counter = 0
brace_counter = 0
previous_state = ""

def Advance_To_Function_Name(scanner,text):
	
	print "Detected function name '%s'" % text
	
	scanner.begin("function_scope_state_parameters_start")

def Advance_To_Function_Params(scanner,text):
	
	print "Advancing to parameter list"
	
	scanner.begin("function_scope_state_parameters_start")

def Function_Definition_Start(scanner,text):
	
	global previous_state
	
	print "Function found: '%s'" % text
	
	previous_state = scanner.state_name
	
	scanner.begin("function_scope_state_space_start")

def Advance_To_Function_Params_Name(scanner,text):
	
	print "Advancing to parameter list."
	
	global brace_counter
	brace_counter = 0
	
	scanner.begin("function_scope_state_parameters_name")

def Advance_To_Function_Scope(scanner,text):
	
	global bracket_counter
	
	print "Advancing to function scope"
	
	Function_Open_Bracket(scanner,text)
	
	bracket_counter = scanner.nesting_level
	
	scanner.begin("function_scope")
	
def Function_Open_Bracket(scanner,text):
	
	scanner.cp_open_bracket(text)
	
def Function_Close_Bracket(scanner,text):
	
	global previous_state
	global bracket_counter
	
	scanner.cp_close_bracket(text)
	
	if scanner.nesting_level < bracket_counter:
		
		print "Leaving function scope."
		
		scanner.begin(previous_state)

def Open_Brace(scanner,text):
	
	global brace_counter
	brace_counter = brace_counter + 1

def Close_Brace(scanner,text):
	
	global brace_counter
	brace_counter = brace_counter - 1
	
	if brace_counter < 0:
		
		print "Parameter list complete."
		
		scanner.begin("function_scope_bracket")

function_scope_state_parameters_name = State(
	"function_scope_state_parameters_name", [
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

function_scope_state_parameters_start = State(
	"function_scope_state_parameters_start", [
		(whitespace_chars,   IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(Str("("), Advance_To_Function_Params_Name)
	]
)

function_scope_state_space = State(
	"function_scope_state_space_start", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(valid_name_chars,Advance_To_Function_Name)
	]
)

function_scope_bracket = State(
	"function_scope_bracket", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(Str("{"),Advance_To_Function_Scope)
	]
)

function_scope = State(
	"function_scope", [
		(Rep(AnyBut("{}")),IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(c_bracket_open, Function_Open_Bracket),
		(c_bracket_closed, Function_Close_Bracket)
	]
)

#<type> <modifier list> <name>(
function_search_pattern = Str("public","private") + force_whitespace + valid_name_chars + Opt(Rep(force_whitespace + valid_name_chars)) + whitespace + Opt(Rep(Str("*"))) +  force_whitespace

token_tuple = (function_search_pattern, Function_Definition_Start)

lexicon_list_states = []
lexicon_list_states.append(function_scope_state_space)
lexicon_list_states.append(function_scope_state_parameters_start)
lexicon_list_states.append(function_scope_state_parameters_name)
lexicon_list_states.append(function_scope_bracket)
lexicon_list_states.append(function_scope)


#master lexicon list
lexicon_list = []

lexicon_list = lexicon_list + lexicon_list_states

def Get_Token_Tuples():
	
	return [token_tuple]

def Get_Lexicon_List():
	
	return lexicon_list

		
