import os
import sys
import re
import argparse

from Utils import find_modules

warning = "config.ini contains some duplicate settings between filetypes.\n \
    This prevents the cleaner from distinguishing between source files.\n \
        Consider adding prefixes, suffixes, or directories to config.ini filetype \
            settings to enable the cleaner to work properly."

class Cleaner:
    def __init__( self, args, mod_configs ):
        self.args = args
        self.modules = None
        self.configs = mod_configs

        if not self.files_are_distinguishable():
            print( warning )

        self.file_clean_list = list()

        self.root_dir = False
        self.recurse = False
        self.dry_run = False
        self.runners_flag = False
        self.builds_flag = False
        self.results_flag = False
        self.all_flag = False
        self.venv_flag = False
        self.verbose = False
        self.scripts_flag = False

        self.read_args()

    def read_args( self ):
        # descriptionText = 'Deletes selected module components and artifacts'
        # print( self.args )

        self.root_dir = self.args.module
        self.recurse = self.args.recurse

        # Default settings when no --module arg is given
        if self.root_dir is None:
            self.root_dir = '.'
            self.recurse = True

        if modules := find_modules( self.root_dir, self.recurse, self.configs ):
            self.modules = [os.path.dirname( os.path.normpath( module ) ) for module in modules if modules]

        if self.args.dry is not None:
            self.dry_run = self.args.dry

        if self.args.runners:
            self.runners_flag = self.args.runners

        if self.args.results:
            self.results_flag = self.args.results

        if self.args.builds:
            self.builds_flag = self.args.builds

        if self.args.scripts:
            self.scripts_flag = self.args.scripts

        if (self.runners_flag is False) and \
            (self.results_flag is False) and \
            (self.builds_flag is False) and \
            (self.scripts_flag is False):
            self.all_flag = True

        elif self.args.all is None or self.args.all is True:
            self.all_flag = self.args.all
            # Override other settings to honor "all" functionality
            self.runners_flag = True
            self.builds_flag = True
            self.results_flag = True
            self.scripts_flag = True

        if self.args.venv is not None and self.args.venv is True:
            self.venv_flag = True

        if self.args.verbose is not None and self.args.verbose is True:
            self.verbose = True

        # print( "self.root_dir", self.root_dir )
        # print( "self.recurse", self.recurse )
        # print( "self.dry_run", self.dry_run )
        # print( "self.runners_flag", self.runners_flag )
        # print( "self.builds_flag", self.builds_flag )
        # print( "self.results_flag", self.results_flag )
        # print( "self.all_flag", self.all_flag )
        # print( "self.venv_flag", self.venv_flag )
        # print( "self.verbose", self.verbose )
        # print( "self.scripts", self.scripts_flag )

    def delete_file( self, path ):
        if os.path.exists( path ):
            if self.verbose:
                print( path )
            os.remove( path )
        else:
            print("The file", path, "does not exist")
            # os.rmdir() works only for empty directories

    def do_cleaning( self ):
        # print( self.file_clean_list )
        if self.file_clean_list:
            if self.dry_run is False:
                print("cleaning..")
                [self.delete_file(fi) for fi in self.file_clean_list]
            else:
                print("would clean:")
                [print(fi) for fi in self.file_clean_list]
        else:
            print( "nothing to clean" )

    def find_files_types( self, dir='.', prefix='', suffix='', extension='' ):
        matches = list()
        pattern = prefix + ".*" + suffix + extension
        # print(pattern)

        for module_path in self.modules:
            for root, dirs, files in os.walk( os.path.join( module_path, dir ) ):
                # print(root,dirs,files)
                [matches.append( os.path.join(root, fi) ) for fi in filter(lambda x: re.match(pattern, x), files)]
        # print(matches)
        return matches

    def find_runners( self ):
        runners = list()
        runners = self.find_files_types( self.configs["runner_dir"], \
                                            self.configs["runner_src_prefix"], \
                                            self.configs["runner_src_suffix"], \
                                            ".c", \
                                        )
        # print(runners)
        return runners

    def find_builds( self ):
        builds = list()
        # For linux builds only
        builds = self.find_files_types( self.configs["exe_dir"], \
                                            ".", \
                                            ".", \
                                            ".out", \
                                        )
        # print(builds)
        return builds

    def find_results( self ):
        results = list()
        results = self.find_files_types( self.configs["results_dir"], \
                                            self.configs["results_txt_prefix"], \
                                            self.configs["results_txt_suffix"], \
                                            ".txt", \
                                        )
        # print(results)
        return results

    def find_scripts( self, filename ):
        scripts = list()

        for module_path in self.modules:
            script_path = os.path.join( module_path, filename )
            script_path = script_path.strip("/")
            script_path = os.path.normpath( script_path )

            if os.path.isfile( script_path ):
                scripts.append( script_path )
        # print(scripts)
        return scripts

    def find_files( self ):
        temp_list = list()

        if self.modules is None:
            print("no modules found")
            sys.exit()

        if self.all_flag or self.runners_flag:
            # Look for runners and add to file delete list if any are found
            runners = self.find_runners()
            [temp_list.append( runner ) for runner in runners if runners is not None]
        if self.all_flag or self.builds_flag:
            builds = self.find_builds()
            [temp_list.append( build ) for build in builds if builds is not None]
        if self.all_flag or self.results_flag:
            results = self.find_results()
            [temp_list.append( result ) for result in results if results is not None]
        if self.all_flag or self.scripts_flag:
            scripts = self.find_scripts( self.configs["test_script_name"] )
            [temp_list.append( script ) for script in scripts if scripts is not None]

        self.file_clean_list = sorted( temp_list )

    def files_are_distinguishable( self ):
        result = True
        if self.configs["runner_dir"] == self.configs["test_dir"] \
            and self.configs["runner_src_prefix"] == self.configs["test_src_prefix"] \
            and self.configs["runner_src_suffix"] == self.configs["test_src_suffix"]:
            result = False

        if self.configs["runner_dir"] == self.configs["results_dir"] \
            and self.configs["runner_src_prefix"] == self.configs["results_txt_prefix"] \
            and self.configs["runner_src_suffix"] == self.configs["results_txt_suffix"]:
            result = False

        if self.configs["test_dir"] == self.configs["results_dir"] \
            and self.configs["test_src_prefix"] == self.configs["results_txt_prefix"] \
            and self.configs["test_src_suffix"] == self.configs["results_txt_suffix"]:
            result = False

        return result
