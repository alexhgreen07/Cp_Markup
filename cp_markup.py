## @package cp_markup
# @brief This file is the main file to execute when translating
# C+ code to to C code. 

import sys
import os
import time

current_path, current_file = os.path.split(os.path.abspath(__file__))
sys.path.append(current_path + "/lib")

import cp_markup_lib
from cp_markup_lib import *

current_path, current_file = os.path.split(os.path.abspath(__file__))

## @brief This is the main function for the translator.
# It will parse through a file, output the parsed
# elements, and generate the appropriate .h and .c files.
def main():
	
	
	run_time_start = time.time()
	
    
	print "Start plex test"
	print ""

	print "Creating lexicon"
	print ""
	
	#create the master program object which will store all
	#the application objects.
	cp_program_object = Cp_Program("test_program")
	
	filename = current_path + "/test_code/test_file.cp"
	
	scanned_file_count = 0
	files_to_scan = [filename]
	files_scanned = []
	
	while len(files_to_scan) > 0:
	
		
		current_scanned_filepath = files_to_scan[0]
		
		f = open(current_scanned_filepath, "r")
		scanner = CpScanner(f, current_scanned_filepath)
	
		print "Parsing '" + current_scanned_filepath + "'"
		print ""
	
		while True:
			
			#attempt to read the next token
			try:
			
			
	    			token = scanner.read()
	    			
	    		except Exception as exc:
	    		
	    			print "Parsing error: '%s'" % exc
	    			break
	    		
	    		#print the token
	    		print token
	    		sys.stdout.flush()
	    		
	    		#if the reader is at the end of file
	    		if token[0] is None:
	    		
				break
		
		
		#add all new paths found to import
		for import_path in scanner.import_file_list:
			
			scanned_file_path, scanned_file = os.path.split(os.path.abspath(current_scanned_filepath))
			
			#if it has not already been scanned
			if not import_path in files_scanned:
			
				print "Found new path to import '%s'" % (scanned_file_path + "/" + import_path)
			
				files_to_scan.append(scanned_file_path + "/" + import_path)
		
		#track the files that have been scanned
		files_scanned.append(current_scanned_filepath)
		files_to_scan.remove(current_scanned_filepath)
		
		del f
		del scanner
		
		print ""

	
	elapsed = (time.time() - run_time_start)
	
	print "runtime elapsed: " + str(elapsed)
	
	elapsed = (time.time() - time_start)
	
	print "total time elapsed: " + str(elapsed)
	
	print ""
	print "Manifest:"
	print ""
	
	print "import*************"
	for path in files_scanned:
		
		print "import '%s'" % path
	
	
	
	print ""
	print "Ending plex test"

if __name__ == "__main__":
	
	main()
    	
