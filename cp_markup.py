import sys
import os
import time

current_path, current_file = os.path.split(os.path.abspath(__file__))
sys.path.append(current_path + "/lib")

import cp_markup_lib
from cp_markup_lib import *


if __name__ == "__main__":
    
    	run_time_start = time.time()
	
    
	print "Start plex test"
	print ""

	print "Creating lexicon"
	print ""
	
	#create the master program object
	cp_program_object = Cp_Program("test_program")
	
	filename = "test_file.cp"
	
	scanned_file_count = 0
	files_to_scan = [filename]
	files_scanned = []
	
	while len(files_to_scan) > 0:
	
	
		f = open(files_to_scan[0], "r")
		scanner = CpScanner(f, files_to_scan[0])
	
		print "Parsing '" + files_to_scan[0] + "'"
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
			
			#if it has not already been scanned
			if not import_path in files_scanned:
			
				print "Found new path to import '%s'" % import_path
			
				files_to_scan.append(import_path)
		
		#track the files that have been scanned
		files_scanned.append(files_to_scan[0])
		files_to_scan.remove(files_to_scan[0])
		
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
