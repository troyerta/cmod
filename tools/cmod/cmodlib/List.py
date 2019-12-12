import os
import sys
import argparse

from Utils import find_modules

class List:
	def __init__( self, args ):
		self.modules = None
		self.list_modules( args )

	def list_modules( self, argv ):
		descriptionText = 'Prints a list of modules found under a passed-in directory'
		usageText = 'cmod list [--m|--r]'

		parser = argparse.ArgumentParser( description=descriptionText, usage=usageText )

		parser.add_argument( '--module', '-module', '--m', '-m', \
		type=str, \
		dest='module', \
		help='--module example:' )

		parser.add_argument( '--r', '-r', \
		dest='recurse', \
		help='--recurse example:', \
		action='store_true' )

		args = parser.parse_args( argv )
		self.root_dir = args.module
		self.recurse = args.recurse

		if self.root_dir is None:
			self.root_dir = '.'
			self.recurse = True

		# This function can also be used to make Module objects when we need to do some testing
		modules = find_modules( self.root_dir, self.recurse )

		if modules:
			self.modules = modules
			for module in modules:
				print( os.path.basename( os.path.dirname( os.path.normpath( module ) ) ) )
		else:
			print("No modules found")