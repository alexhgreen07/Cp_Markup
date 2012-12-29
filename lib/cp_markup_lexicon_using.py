## @package cp_markup_lexicon_using
# @brief This file contains all lexical objects and functions for parsing
# C+ using statements.

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

## @brief This function is triggered when the starting keyword of the using statement is found.
def Using_Definition_Start(scanner,text):
	
	global previous_state
	previous_state = scanner.state_name
	
	scanner.begin("using_scope_state_name")
	
## @brief This function is triggered when the name of the namespace being used is found.
def Using_Definition_Name(scanner,text):
	
	print "Using namespace '%s'" % text
	
	scanner.begin("using_scope_state_terminator")

## @brief This function is triggered when the using statement is complete.
def Using_Definition_Complete(scanner,text):
	
	global previous_state
	
	scanner.begin(previous_state)

## @brief This is a Plex state object for detecting the namespace name being used.
using_scope_state_name = State(
	"using_scope_state_name", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(valid_name_chars + Opt(Rep(whitespace + Str("::") + valid_name_chars)),Using_Definition_Name)
	]
)

## @brief This is a Plex state object for detecting the end of the using statement.
using_scope_state_terminator = State(
	"using_scope_state_terminator", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(Str(";"),Using_Definition_Complete)
	]
)

## @brief This is the token for detecting the start of the using definition.
token_tuple = (Str("using") + force_whitespace, Using_Definition_Start)

## @brief This is a list of all states used for parsing the using definition.
lexicon_list_states = []
lexicon_list_states.append(using_scope_state_name)
lexicon_list_states.append(using_scope_state_terminator)

## @brief This is the master lexicon list for parsing using definitions.
lexicon_list = []
lexicon_list = lexicon_list + lexicon_list_states

def Get_Token_Tuples():
	
	return [token_tuple]

def Get_Lexicon_List():
	
	return lexicon_list

		
