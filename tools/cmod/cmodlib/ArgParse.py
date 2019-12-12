import os
import sys
import argparse

help_types = [ 'help', 'h', '-h', '--h', '--help' ]
generate_types = [ 'generate', 'gen' ]
list_types = [ 'list', 'l' ]
tree_types = [ 'tree', 'tr' ]
build_types = [ 'build', 'bld' ]
report_types = [ 'report', 'rpt' ]
test_types = [ 'test', 'tst' ]
stat_types = [ 'stat', 'st' ]
format_types = [ 'format', 'fmt' ]
analyze_types = [ 'analyze', 'an' ]
tdd_types = [ 'td', 'tdd' ]

def handle_help( args, global_cfg, mod_cfg ):
	print("handling help")

def handle_generate( args, global_cfg, mod_cfg ):
	from Generate import Generate
	print("handling generate")
	# Sets up an argparser and runs
	gen = Generate()

def handle_list( args, global_cfg, mod_cfg ):
	from List import List
	list_runner = List( args )

def handle_tree( args, global_cfg, mod_cfg ):
	from Tree import tree
	print("handling tree")
	tree( args )

def handle_build( args, global_cfg, mod_cfg ):
	print("handling build")

def handle_report( args, global_cfg, mod_cfg ):
	print("handling report")

def handle_test( args, global_cfg, mod_cfg ):
	print("handling test")

def handle_stat( args, global_cfg, mod_cfg ):
	print("handling stat")

def handle_format( args, global_cfg, mod_cfg ):
	print("handling format")

def handle_analyze( args, global_cfg, mod_cfg ):
	print("handling analyze")

def handle_tdd( args, global_cfg, mod_cfg ):
	print("handling tdd")

action_types = [ 'help', 'generate', 'list', 'tree', 'build', 'report', 'test', 'stat', 'format', 'analyze', 'td' ]
handlers = [ handle_help, handle_generate, handle_list, handle_tree, handle_build, handle_report, handle_test, handle_stat, handle_format, handle_analyze, handle_tdd ]
# cmod_task_dict = dict(zip(action_types, action_handlers))

def get_normalized_command_index( input_cmd ):
	if input_cmd in help_types:
		from Help import Help
		return 0
	elif input_cmd in generate_types:
		return 1
	elif input_cmd in list_types:
		return 2
	elif input_cmd in tree_types:
		return 3
	elif input_cmd in build_types:
		return 4
	elif input_cmd in report_types:
		return 5
	elif input_cmd in test_types:
		return 6
	elif input_cmd in stat_types:
		return 7
	elif input_cmd in format_types:
		return 8
	elif input_cmd in analyze_types:
		return 9
	elif input_cmd in tdd_types:
		return 10
	else:
		print("invalid cmod command")
		sys.exit()

class ArgParser:
	def __init__( self, sys_args=None, global_configs=None, module_configs=None ):
		self.args = sys_args
		self.global_config = global_configs
		self.module_config = module_configs

	def cmod_entry(self):
		# if self.args[0] not in action_types:
			# print("invalid cmod command")
			# sys.exit()
		idx = get_normalized_command_index( self.args[0] )
		self.args.remove( self.args[0] )
		handlers[ idx ]( self.args, self.global_config, self.module_config )
		sys.exit()


