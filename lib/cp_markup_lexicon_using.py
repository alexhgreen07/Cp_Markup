import sys
import os
import time

import cp_markup_lexicon_global
from cp_markup_lexicon_global import *

current_path, current_file = os.path.split(os.path.abspath(__file__))
sys.path.append(current_path + "/plex-2.0.0dev/src")

import plex
from plex import *

brace_counter = 0
previous_state = ""

def Using_Definition_Start(scanner,text):
	
	global previous_state
	previous_state = scanner.state_name
	
	scanner.begin("using_scope_state_name")
	
def Using_Definition_Name(scanner,text):
	
	print "Using namespace '%s'" % text
	
	scanner.begin("using_scope_state_terminator")

def Using_Definition_Complete(scanner,text):
	
	global previous_state
	
	scanner.begin(previous_state)

using_scope_state_name = State(
	"using_scope_state_name", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(valid_name_chars + Opt(Rep(whitespace + Str("::") + valid_name_chars)),Using_Definition_Name)
	]
)

using_scope_state_terminator = State(
	"using_scope_state_terminator", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(Str(";"),Using_Definition_Complete)
	]
)

token_tuple = (Str("using") + force_whitespace, Using_Definition_Start)

lexicon_list_states = []
lexicon_list_states.append(using_scope_state_name)
lexicon_list_states.append(using_scope_state_terminator)

#master lexicon list
lexicon_list = []

lexicon_list = lexicon_list + lexicon_list_states

def Get_Token_Tuples():
	
	return [token_tuple]

def Get_Lexicon_List():
	
	return lexicon_list

		
