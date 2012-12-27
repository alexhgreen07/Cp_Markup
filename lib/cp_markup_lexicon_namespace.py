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

current_path, current_file = os.path.split(os.path.abspath(__file__))
sys.path.append(current_path + "/plex-2.0.0dev/src")

import plex
from plex import *

bracket_counter = 0
brace_counter = 0
previous_state = ""

def Advance_To_Namespace_Name(scanner,text):
	
	print "Detected namespace name '%s'" % text
	
	scanner.begin("namespace_scope_state_bracket")
	

def Namespace_Definition_Start(scanner,text):
	
	previous_state = scanner.state_name
	
	scanner.begin("namespace_scope_state_space_start")

def Advance_To_Namespace_Scope(scanner,text):
	
	global bracket_counter
	
	Namespace_Open_Bracket(scanner,text)
	bracket_counter = scanner.nesting_level
	
	print "In namespace scope at nesting level %d" % scanner.nesting_level
	
	scanner.begin("namespace_scope")

def Namespace_Open_Bracket(scanner,text):
	
	scanner.cp_open_bracket(text)

def Namespace_Close_Bracket(scanner,text):
	
	global bracket_counter
	
	scanner.cp_close_bracket(text)
	
	if scanner.nesting_level < bracket_counter:
		
		print "Leaving namespace scope."
		
		scanner.begin(previous_state)
	

namespace_scope_state_space = State(
	"namespace_scope_state_space_start", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(valid_name_chars + Opt(Rep(whitespace + Str("::") + valid_name_chars)),Advance_To_Namespace_Name)
	]
)

namespace_scope_state_bracket = State(
	"namespace_scope_state_bracket", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(Str("{"),Advance_To_Namespace_Scope)
	]
)

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

token_tuple = (Str("namespace") + force_whitespace, Namespace_Definition_Start)

lexicon_list_states = []
lexicon_list_states.append(namespace_scope_state_space)
lexicon_list_states.append(namespace_scope_state_bracket)
lexicon_list_states.append(namespace_scope)


#master lexicon list
lexicon_list = []

lexicon_list = lexicon_list + lexicon_list_states

def Get_Token_Tuples():
	
	return [token_tuple]

def Get_Lexicon_List():
	
	return lexicon_list

		
