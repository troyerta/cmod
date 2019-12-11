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

action_types = [ 'help', 'generate', 'list', 'tree', 'build', 'report', 'test', 'stat', 'format', 'analyze', 'td' ]
cmd_modules = [ Help, Generate, List, Tree, Build, Report, Test, Stat, Format, Analyze, TestDrive ]
action_handlers = [ generate, generate, test, list_modules ]
cmod_task_dict = dict(zip(action_types, action_handlers))

def normalize_command( input_cmd ):
	if input_cmd in help_types:
		return 0
	if input_cmd in generate_types:
		return 1
	if input_cmd in list_types:
		return 2
	if input_cmd in tree_types:
		return 3
	if input_cmd in build_types:
		return 4
	if input_cmd in report_types:
		return 5
	if input_cmd in test_types:
		return 6
	if input_cmd in stat_types:
		return 7
	if input_cmd in format_types:
		return 8
	if input_cmd in analyze_types:
		return 9
	if input_cmd in tdd_types:
		return 10

class ArgParser:
	def __init__( self, sys_args=None, global_configs=None, module_configs=None ):
		self.args = sys_args
		self.global_config = global_configs
		self.module_config = module_configs

	def cmod_entry(self):
		if self.args[0] not in action_types:
			print("invalid cmod command")
			sys.exit()
		cmd = self.args[0]
		self.args.remove( cmd )


