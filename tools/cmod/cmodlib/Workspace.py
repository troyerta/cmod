import os
import sys
import re
import argparse

from Module import Module

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
    def __init__(self, args=None, global_cfg=None, mod_cfg=None):
        self.root_dir = None
        self.global_cfg = global_cfg
        self.mod_cfg = mod_cfg
        self.verbosity = int(self.mod_cfg["default_verbosity"])
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


    def find_module_dir( self, module ):
        matches = list()
        script = os.path.join( os.path.normpath(module), 'test' )
        if os.path.isfile(script):
            matches.append( script )
        return matches

    def find_module_dirs_recursive( self, module ):
        pattern = "^test$"
        matches = list()
        for root, dirs, files in os.walk( module ):
            [matches.append( os.path.join(root, file) ) for file in filter(lambda x: re.match(pattern, x), files)]
        return matches

    def find_modules( self, root_dir, recurse ):
        matches = list()
        if recurse is True:
            matches = self.find_module_dirs_recursive( root_dir )
        else:
            matches = self.find_module_dir( root_dir )
        return matches

    def get_workspace_module_paths( self, argv ):
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

        parser.add_argument( '--v', '-v', \
        type=int, \
        dest='verbosity', \
        help='--verbosity example:' )

        args = parser.parse_args( argv )
        self.root_dir = args.module
        self.recurse = args.recurse
        if args.verbosity is not None:
            self.verbosity = args.verbosity

        if self.root_dir is None:
            self.root_dir = '.'
            self.recurse = True
        # This function can also be used to make Module objects when we need to do some testing
        if self.verbosity > 1:
            print("Finding modules..", end='')
        modules = self.find_modules( self.root_dir, self.recurse )
        modules = [os.path.dirname( os.path.normpath( module ) ) for module in modules if modules]
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
        module_objs = [Module( module, self.mod_cfg, self.verbosity ) for module in self.module_path_list]
        if self.verbosity > 1:
            print("[" + str(len(module_objs)) + "]")
        return module_objs

    def find_wksp_test_src_files( self ):
        [mod.find_test_src_files() for mod in self.module_objs]

    def find_wksp_tests_and_groups( self ):
        [mod.find_tests_and_groups() for mod in self.module_objs]

    def gen_wksp_test_runners( self ):
        [mod.gen_test_runner() for mod in self.module_objs]

    def run_module_test( self, module, progress ):
        if self.verbosity > 1:
            print(make_progress_str(self.num_modules, progress ) + " Testing " + module.path)
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
            print( "\033[92m PASS:", self.passed, "\033[91m FAIL:", self.failed, "\033[93m IGNORE:", self.ignored, "\033[94m TOTAL:", self.total, "tests", "\033[00m", "in", str(self.num_modules), "modules" )
            print( "-------------------------------------------------------------" )
