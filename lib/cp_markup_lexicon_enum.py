import sys
import os
import time

import cp_markup_lexicon_global
from cp_markup_lexicon_global import *
import cp_markup_lexicon_class

current_path, current_file = os.path.split(os.path.abspath(__file__))
sys.path.append(current_path + "/plex-2.0.0dev/src")

import plex
from plex import *

brace_counter = 0
previous_state = ""

def Advance_To_Enum_Name(scanner,text):
	
	global previous_state
	
	print "Detected enum name '%s'" % text
	
	scanner.begin(previous_state)

def Enum_Definition_Start(scanner,text):
	
	global previous_state
	
	print "%s keyword found." % text
	
	previous_state = scanner.state_name
	
	scanner.begin("enum_scope_state_space_start")

enum_scope_state_space = State(
	"enum_scope_state_space_start", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(valid_name_chars,Advance_To_Enum_Name)
	]
)

token_tuple = (Str("enum") + force_whitespace, Enum_Definition_Start)

lexicon_list_states = []
lexicon_list_states.append(enum_scope_state_space)


#master lexicon list
lexicon_list = []

lexicon_list = lexicon_list + lexicon_list_states

def Get_Token_Tuples():
	
	return [token_tuple]

def Get_Lexicon_List():
	
	return lexicon_list

		
