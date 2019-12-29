import os
import sys
import re
import argparse

class Cleaner:
    def __init__( self, args, mod_objs, mod_configs ):
        self.args = args
        self.modules = mod_objs
        self.configs = mod_configs

        self.file_clean_list = list()

        self.dry_run = False
        self.runners_flag = False
        self.builds_flag = False
        self.results_flag = False
        self.all_flag = False
        self.venv_flag = False
        self.verbose = False

    def read_args( self ):
        descriptionText = 'Deletes selected module components and artifacts'
        usageText = 'cmod clean [--m|--r]'

        parser = argparse.ArgumentParser( description=descriptionText, usage=usageText )

        parser.add_argument( '--dry', '-dry', \
        dest='dry', \
        help='--dry example:', \
        action='store_true' )

        parser.add_argument( '--runners', '-runners', \
        dest='runners', \
        help='--runners example:', \
        action='store_true' )

        parser.add_argument( '--builds', '-builds', \
        dest='builds', \
        help='--builds example:', \
        action='store_true' )

        parser.add_argument( '--results', '-results', \
        dest='results', \
        help='--results example:', \
        action='store_true' )

        parser.add_argument( '--all', '-all', \
        dest='all', \
        help='--all example:', \
        action='store_true' )

        parser.add_argument( '--venv', '-venv', \
        dest='venv', \
        help='--venv example:', \
        action='store_true' )

        parser.add_argument( '--verbose', '-verbose', \
        dest='verbose', \
        help='--verbose example:', \
        action='store_true' )

        temp_args = parser.parse_args( self.args )
        # print(temp_args)

        if temp_args.dry is not None and temp_args.dry is True:
            self.dry_run = True

        if temp_args.runners is not None and temp_args.runners is True:
            self.runners_flag = True

        if temp_args.results is not None and temp_args.results is True:
            self.results_flag = True

        if temp_args.builds is not None and temp_args.builds is True:
            self.builds_flag = True

        if temp_args.all is not None and temp_args.all is True:
            self.all_flag = True
            # Override other settings to honor "all" functionality
            self.runners_flag = True
            self.builds_flag = True
            self.results_flag = True

        if temp_args.venv is not None and temp_args.venv is True:
            self.venv_flag = True

        if temp_args.verbose is not None and temp_args.verbose is True:
            self.verbose = True

    def delete_file( self, path ):
        if os.path.exists( path ):
            print( path )
            os.remove( path )
        else:
            print("The file", path, "does not exist")
            # os.rmdir() works only for empty directories

    def do_cleaning( self ):
        if self.dry_run is False:
            print("\nCleaning..")
            [self.delete_file(fi) for fi in self.file_clean_list]

        else:
            print("\nWould delete")
            [print(fi) for fi in self.file_clean_list]

    def find_files_types( self, dir, prefix, suffix, extension ):
        matches = list()
        for module_obj in self.modules:
            pattern = prefix + ".*" + suffix + extension
            # print(pattern)
            for root, dirs, files in os.walk( os.path.join( module_obj.path, dir ) ):
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

    def find_files( self ):
        temp_list = list()

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

        self.file_clean_list = sorted( temp_list )

