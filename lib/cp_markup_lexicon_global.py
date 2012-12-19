import sys
import os
import time

import cp_language_objects

current_path, current_file = os.path.split(os.path.abspath(__file__))
sys.path.append(current_path + "/../plex-2.0.0dev/src")

import plex
from plex import *

letter = Range("AZaz")
digit = Range("09")
underscore = Range("__")
valid_name_chars = Rep1(letter | digit | underscore)

#whitespace characters
whitespace_chars = Str(" ","\t","\n")
whitespace = Rep(whitespace_chars)

#BUG this must be fixed to force whitespace
force_whitespace = Rep1(whitespace_chars)
#force_whitespace = whitespace

#define the basic C keywords
c_keywords_branches = Str(
	"if", 
	"else",
	"switch",
	"break",
	"continue",
	"goto")

#define the basic C types
c_base_types = Str(
	"void",
	"char",
	"short",
	"int",
	"long",
	"long long",
	"float",
	"double",
	"long double")

#get the type modifiers
c_base_type_modifiers = Str(
	"unsigned",
	"signed")

#define the special C types
c_special_types = Str(
	"struct",
	"union")

#storage duration identifiers
c_storage_durations = Str(
	"auto",
	"register",
	"extern")

#static duration is separately defined
c_static_duration = Str("static")

#brackets
c_bracket_open = Str("{")
c_bracket_closed = Str("}")

#braces
c_brace_open = Str("(")
c_brace_closed = Str(")")

#array braces
c_array_brace_open = Str("[")
c_array_brace_closed = Str("]")

#comment delimiters
c_comment_open = Str("/*")
c_comment_closed = Str("*/")

#address operators
c_pointer_operators = Str(
	"*",
	"&")

#end of instruction operator
c_end_instruction = Str(";")

#C+ types
cp_special_types = Str(
	"class",
	"namespace")

#define comments
line_comment = Str("//") + Rep(AnyBut("\n"))
c_comment_block = Str("/*") + Rep(AnyBut("*/")) + Str("*/")
c_comments = c_comment_block | line_comment

preprocessor = Str("#") + Rep(AnyBut("\n"))
		
