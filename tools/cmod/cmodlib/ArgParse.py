import os
import sys
import argparse
import re

sys.path.insert(1, 'tools/cmod/cmodlib/generators')

help_types     = [ 'help', 'h', '-h', '--h', '--help' ]
generate_types = [ 'generate', 'gen' ]
clean_types    = [ 'clean' ]
list_types     = [ 'list', 'l' ]
tree_types     = [ 'tree', 'tr' ]
build_types    = [ 'build', 'bld' ]
report_types   = [ 'report', 'rpt' ]
stat_types     = [ 'stat', 'st' ]
format_types   = [ 'format', 'fmt' ]
analyze_types  = [ 'analyze', 'an' ]
tdd_types      = [ 'td', 'tdd', 'test', 'tst' ]

def handle_help( args, global_cfg, mod_cfg ):
    print("handling help")

# Generate a module, file, or snippet
def handle_generate( args, global_cfg, mod_cfg ):
    from Generate import Generate
    from source_generator import print_source
    from header_generator import print_header
    from test_source_generator import print_test_source
    from tdd_script_generator import print_tdd_script
    from makefile_generator import print_makefile
    # Make sure raw path arg string has no leading slash
    module_dir = args[0].lstrip("/")

    # print( args )
    print_source( module_dir, mod_cfg, global_cfg )
    print_header( module_dir, mod_cfg, global_cfg )
    print_test_source( module_dir, mod_cfg, global_cfg )
    print_makefile( module_dir, mod_cfg, global_cfg )
    print_tdd_script( module_dir, mod_cfg, global_cfg )

def handle_list( args, global_cfg, mod_cfg ):
    from Workspace import Workspace
    wksp = Workspace( args=args, mod_cfg=mod_cfg )
    wksp.print_module_names()

def handle_tree( args, global_cfg, mod_cfg ):
    from Tree import tree
    tree( args )

def handle_report( args, global_cfg, mod_cfg ):
    print("handling report\n")

def handle_stat( args, global_cfg, mod_cfg ):
    print("handling stat\n")

def handle_format( args, global_cfg, mod_cfg ):
    print("handling format\n")

def handle_analyze( args, global_cfg, mod_cfg ):
    print("handling analyze\n")

def handle_tdd( args, global_cfg, mod_cfg ):
    from Workspace import Workspace
    wksp = Workspace( args, mod_cfg=mod_cfg )
    wksp.find_wksp_test_src_files()
    wksp.find_wksp_tests_and_groups()
    wksp.gen_wksp_test_runners()
    wksp.run_wksp_tests()
    wksp.calculate_test_result_totals()
    wksp.print_test_summary()

def handle_clean( args, global_cfg, mod_cfg ):
    from Clean import Cleaner
    cleaner = Cleaner( args, mod_cfg )
    cleaner.read_args()
    cleaner.find_files()
    cleaner.do_cleaning()

action_types = [ 'help', 'generate', 'list', 'tree', 'report', 'stat', 'format', 'analyze', 'tdd', 'clean' ]
action_handlers = [ handle_help, handle_generate, handle_list, handle_tree,  handle_report, handle_stat, handle_format, handle_analyze, handle_tdd, handle_clean ]
cmod_cmd_dict = dict(zip(action_types, action_handlers))

def get_normalized_command_index( input_cmd ):
    if input_cmd in help_types:
        from Help import Help
        return action_types[0]
    elif input_cmd in generate_types:
        return action_types[1]
    elif input_cmd in list_types:
        return action_types[2]
    elif input_cmd in tree_types:
        return action_types[3]
    elif input_cmd in report_types:
        return action_types[4]
    elif input_cmd in stat_types:
        return action_types[5]
    elif input_cmd in format_types:
        return action_types[6]
    elif input_cmd in analyze_types:
        return action_types[7]
    elif input_cmd in tdd_types:
        return action_types[8]
    elif input_cmd in clean_types:
        return action_types[9]
    else:
        print("invalid cmod command:", "\""+input_cmd+"\"" )
        sys.exit()

class ArgParser:
    def __init__( self, sys_args=None, global_configs=None, module_configs=None ):
        self.args = sys_args
        self.global_config = global_configs
        self.module_config = module_configs

    def cmod_entry(self):
        cmd = get_normalized_command_index( self.args[0] )
        self.args.remove( self.args[0] )
        cmod_cmd_dict[cmd]( self.args, self.global_config, self.module_config )
        sys.exit()
