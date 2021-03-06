import os
import sys
import re
import argparse

from Module import Module, do_test_cycle
from Utils import find_modules

# This class does has all the same stuff as
# the Module class does, but with lists of
# Modules instead

def make_progress_str( total, progress ):
    total_str = str(total)
    progress_str = str(progress)
    total_str_width = len(total_str)
    progress_str_width = len(progress_str)

    output = '['
    for x in range((total_str_width - progress_str_width)):
        output += ' '
    output += progress_str + "/" + total_str + "]"
    return output

class Workspace:
    def __init__(self, args=None, configs=None, mod_cfg=None):
        self.root_dir = None
        self.configs = configs
        self.verbosity = int(self.configs["GLOBAL"]["default_test_verbosity"])
        self.module_path_list = self.get_workspace_module_paths( args )
        self.module_objs = self.get_module_objects()

        self.num_modules = len(self.module_objs)
        self.num_tests = 0		# Sums of things from all modules
        self.num_passed = 0
        self.num_ignored = 0
        self.num_failed = 0
        self.recurse = None

        self.passed = 0
        self.failed = 0
        self.ignored = 0
        self.total = 0

    def get_workspace_module_paths( self, args ):
        self.root_dir = args.module
        self.recurse = args.recurse
        if args.verbosity is not None:
            self.verbosity = int(args.verbosity)

        if self.root_dir is None:
            self.root_dir = '.'
            self.recurse = True
        # This function can also be used to make Module objects when we need to do some testing
        modules = find_modules( self.root_dir, self.recurse, self.configs )
        modules = [os.path.dirname( os.path.normpath( module ) ) for module in modules if modules]
        if len(modules) > 1 and self.verbosity > 1:
            print("Finding modules..", end='')
        return modules

    def print_module_names( self ):
        if self.module_path_list:
            for module in self.module_path_list:
                print( os.path.basename( module ) )

    def print_module_paths( self ):
        if self.module_path_list:
            for module in self.module_path_list:
                print( module )

    def get_module_paths( self ):
        if self.module_path_list:
            return self.module_path_list
        else:
            print("No modules found")
            return None

    def get_module_objects( self ):
        module_objs = [Module( module, self.configs, self.verbosity ) for module in self.module_path_list]
        if len(module_objs) > 1 and self.verbosity > 1:
            print("[" + str(len(module_objs)) + "]")
        return module_objs

    def find_wksp_test_src_files( self ):
        [mod.find_test_src_files() for mod in self.module_objs]

    def find_wksp_tests_and_groups( self ):
        [mod.find_tests_and_groups() for mod in self.module_objs]

    def gen_wksp_test_runners( self ):
        [mod.gen_test_runner() for mod in self.module_objs]

    def run_module_test( self, module, progress ):
        if self.num_modules > 1 and self.verbosity > 1:
            print(make_progress_str(self.num_modules, progress ) + " Testing " + module.path)
        elif self.verbosity > 1:
            print(" Testing " + module.path)
        sys.stdout.flush()
        module.run_tests()

    def run_wksp_tests( self ):
        [self.run_module_test( mod, count) for count,mod in enumerate( self.module_objs, 1)]

    def accum_module_totals( self, module ):
        self.passed = self.passed + module.get_test_num_passed()
        self.failed += module.get_test_num_failed()
        self.ignored += module.get_test_num_ignored()
        self.total += module.get_test_num_total()

    def calculate_test_result_totals( self ):
        [self.accum_module_totals( mod ) for mod in self.module_objs]

    def print_test_summary( self ):
        if self.verbosity >= 1:
            print( "-------------------------------------------------------------" )
            print( "\033[92m PASS: " + str(self.passed) + \
                "\033[91m FAIL: " + str(self.failed) + \
                "\033[93m IGNORE: " + str(self.ignored) + \
                "\033[94m TOTAL: " + str(self.total) + \
                "\033[00m tests in " + str(self.num_modules) + " modules" )
            print( "-------------------------------------------------------------" )
