import os
import sys
import re
import argparse

from Module import Module

# This class does has all the same stuff as
# the Module class does, but with lists of
# Modules instead

# Difference between this and the Finder class?

class Workspace:
    def __init__(self, args=None, global_cfg=None, mod_cfg=None):
        self.root_dir = None
        self.global_cfg = global_cfg
        self.mod_cfg = mod_cfg
        self.module_path_list = self.get_workspace_module_paths( args )
        self.module_objs = list()
        self.num_modules = 0
        self.num_tests = 0		# Sums of things from all modules
        self.num_passed = 0
        self.num_ignored = 0
        self.num_failed = 0
        self.recurse = None
        self.get_module_objects()

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

        args = parser.parse_args( argv )
        self.root_dir = args.module
        self.recurse = args.recurse

        if self.root_dir is None:
            self.root_dir = '.'
            self.recurse = True
        # This function can also be used to make Module objects when we need to do some testing
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
        self.module_objs = [Module( module, self.mod_cfg ) for module in self.module_path_list]

    def find_wksp_test_src_files( self ):
        [mod.find_test_src_files() for mod in self.module_objs]

    def find_wksp_tests_and_groups( self ):
        [mod.find_tests_and_groups() for mod in self.module_objs]

    def gen_test_runners( self ):
        [mod.gen_test_runner() for mod in self.module_objs]

    def run_tests( self ):
        [mod.run_tests() for mod in self.module_objs]

    def print_test_summary( self ):
        pass