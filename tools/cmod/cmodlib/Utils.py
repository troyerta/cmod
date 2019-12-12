import sys
import os
import re

def find_all_project_modules():
	pattern = "^test$"
	matches = list()

	# Walk the project directory to find all the modules / test-scripts
	for root, dirs, files in os.walk( '.' ):
		for file in filter(lambda x: re.match(pattern, x), files):
			matches.append( os.path.join(root, file) )
	# Don't look for any test file that might exist here in root
	if "./test" in matches:
		matches.remove("./test")
	return matches

def find_module_dir( module ):
	matches = list()
	script = os.path.join( os.path.normpath(module), 'test' )
	if os.path.isfile(script):
		matches.append( script )
	return matches

def find_module_dirs_recursive( module ):
	pattern = "^test$"
	matches = list()

	for root, dirs, files in os.walk( module ):
		for file in filter(lambda x: re.match(pattern, x), files):
			matches.append( os.path.join(root, file) )
	return matches

def find_modules( root_dir, recurse ):
	matches = list()

	if recurse is True:
		matches = find_module_dirs_recursive( root_dir )
	else:
		matches = find_module_dir( root_dir )
	return matches

