## @package cp_markup_lib
# @brief This file contains all required import links for the C+ parser.

import sys
import os
import time

#import the global lexicon library
import cp_markup_lexicon_global
from cp_markup_lexicon_global import *

#import the scanner object
import cp_markup_scanner
from cp_markup_scanner import *

#import the individual language lexicon library elements
import cp_markup_lexicon_class
import cp_markup_lexicon_namespace
import cp_markup_lexicon_import
import cp_markup_lexicon_using
import cp_markup_lexicon_struct_union
import cp_markup_lexicon_enum
import cp_markup_lexicon_function
import cp_markup_lexicon_variable

#import the storage objects for the C+ elements
import cp_markup_language_objects
from cp_markup_language_objects import *

current_path, current_file = os.path.split(os.path.abspath(__file__))
sys.path.append(current_path + "/plex-2.0.0dev/src")

#import the plex parsing library
import plex
from plex import *
		
