import os
import sys

class Module:
	def __init__( self, path ):
		self.path = os.path.normpath( path )

	def __str__(self):
		return str( self.path )
