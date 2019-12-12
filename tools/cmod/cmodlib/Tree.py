from os import listdir, sep
from os.path import abspath, basename, isdir
from sys import argv
from argparse import ArgumentParser

def usage():
	return '''Usage: %s [-f]
Print tree structure of path specified.
Options:
-f      Print files as well as directories
PATH    Path to process''' % basename(argv[0])

def print_tree( dir, padding, print_files=False, isLast=False, isFirst=False):
	if isFirst:
		print( padding[:-1] + dir )
	else:
		if isLast:
			print( padding[:-1] + '└── ' + basename(abspath(dir)) )
		else:
			print( padding[:-1] + '├── ' + basename(abspath(dir)) )
	files = []
	if print_files:
		files = listdir(dir)
	else:
		files = [x for x in listdir(dir) if isdir(dir + sep + x)]
	if not isFirst:
		padding = padding + '   '
	files = sorted(files, key=lambda s: s.lower())
	# [print(file) for file in files]
	if ".git" in files:
		files.remove(".git")
	if ".vscode" in files:
		files.remove(".vscode")
	if "tools" in files:
		files.remove("tools")
	if "unit_test" in files:
		files.remove("unit_test")
	if "unit_testing" in files:
		files.remove("unit_testing")
	# print("")
	# [print(file) for file in files]
	count = 0
	last = len(files) - 1
	for i, file in enumerate(files):
		count += 1
		path = dir + sep + file
		isLast = i == last
		if isdir(path):
			if count == len(files):
				if isFirst:
					print_tree(path, padding, print_files, isLast, False)
				else:
					print_tree(path, padding + ' ', print_files, isLast, False)
			else:
				print_tree(path, padding + '│', print_files, isLast, False)
		else:
			if isLast:
				print( padding + '└── ' + file )
			else:
				print( padding + '├── ' + file )

def tree( args ):
	# No arguments passed in, show module tree for entire project
	if len(args) == 0:
		path = '.'
		print_tree( path, '', False, False, True )
	# Use base module argument to print it's child modules
	# elif len(args) == 2:
	# 	# print( "print just directories" )
	# 	path = args[1]
	# 	if isdir(path):
	# 		print_tree( path, '', False, False, True )
	# 	else:
	# 		print( 'ERROR: \'' + path + '\' is not a directory' )
	# Special case that can print files in some module as well
	# We need to be able to make a test suite, and test case tree as well
	# Will find dirs under the target dir, and for each module, make some Module
	# object that's capable of finding all the test groups and their tests.
	# elif len(args) == 3 and args[1] == '-f':
	# 	# print( "print directories and files" )
	# 	path = args[2]
	# 	if isdir(path):
	# 		print_tree(path, '', True, False, True)
	# 	else:
	# 		print( 'ERROR: \'' + path + '\' is not a directory' )
	else:
		print( usage() )