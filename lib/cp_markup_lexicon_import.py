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

def Advance_To_Import_Name(scanner,text):
	
	print "Detected import string start"
	
	scanner.begin("import_scope_state_filepath")

def Store_Filepath(scanner,text):
	
	print "Filepath to import is '%s'" % text
	
	scanner.import_file_list.append(text)

def Advance_To_Terminator_State(scanner,text):
	
	print "Detected import string end"
	
	scanner.begin("import_scope_state_terminator")

def Import_Definition_Complete(scanner,text):
	
	print "Import definition complete."
	
	global previous_state
	
	scanner.begin(previous_state)

def Import_Definition_Start(scanner,text):
	
	print "Import keyword found."
	
	global previous_state
	previous_state = scanner.state_name
	
	scanner.begin("import_scope_state_space_start")

import_scope_state_space = State(
	"import_scope_state_space_start", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(Str("\"","<"),Advance_To_Import_Name)
	]
)

import_scope_state_filepath = State(
	"import_scope_state_filepath", [
		(Rep(AnyBut("\">")),Store_Filepath),
		(Str("\"",">"),Advance_To_Terminator_State)
	]
)

import_scope_state_terminator = State(
	"import_scope_state_terminator", [
		(whitespace_chars,IGNORE),
		(c_comments,"comment"),
		(preprocessor,"preprocessor"),
		(Str(";"),Import_Definition_Complete)
	]
)

token_tuple = (Str("import"), Import_Definition_Start)

lexicon_list_states = []
lexicon_list_states.append(import_scope_state_space)
lexicon_list_states.append(import_scope_state_filepath)
lexicon_list_states.append(import_scope_state_terminator)


#master lexicon list
lexicon_list = []

lexicon_list = lexicon_list + lexicon_list_states

def Get_Token_Tuples():
	
	return [token_tuple]

def Get_Lexicon_List():
	
	return lexicon_list

		
