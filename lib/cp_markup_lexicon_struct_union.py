import sys
import os
import time

import cp_markup_lexicon_global
from cp_markup_lexicon_global import *
import cp_markup_lexicon_class

current_path, current_file = os.path.split(os.path.abspath(__file__))
sys.path.append(current_path + "/../plex-2.0.0dev/src")

import plex
from plex import *

brace_counter = 0
previous_state = ""

def Advance_To_Struct_Union_Name(scanner,text):
	
	global previous_state
	
	print "Detected struct/union name '%s'" % text
	
	scanner.begin(previous_state)

def Struct_Union_Definition_Start(scanner,text):
	
	global previous_state
	
	print "%s keyword found." % text
	
	previous_state = scanner.state_name
	
	scanner.begin("struct_union_scope_state_space_start")

struct_union_scope_state_space = State(
	"struct_union_scope_state_space_start", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(valid_name_chars,Advance_To_Struct_Union_Name)
	]
)

token_tuple = (Str("struct","union") + force_whitespace, Struct_Union_Definition_Start)

lexicon_list_states = []
lexicon_list_states.append(struct_union_scope_state_space)


#master lexicon list
lexicon_list = []

lexicon_list = lexicon_list + lexicon_list_states

def Get_Token_Tuples():
	
	return [token_tuple]

def Get_Lexicon_List():
	
	return lexicon_list

		
