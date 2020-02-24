import os
import sys
import re
import subprocess

from Unity import TestSrc, TestResult, UnityOutput, TestSummary
from Utils import find_files
from FileGenerator import GeneratedFileDescriptor

def do_test_cycle( module ):
    module.find_test_src_files()
    module.find_tests_and_groups()
    module.gen_test_runner()
    module.run_makefile()
    module.get_test_results()
    module.print_test_results()

class Module:
    def __init__( self, path, configs, verbosity=None ):
        self.path = os.path.normpath( path )
        self.name = os.path.basename( self.path )
        self.config = configs
        self.test_sources = list()    # List of test source objects
        self.test_src_paths = list()  # list of paths
        self.test_groups = list()
        self.test_runner_path = None

        # Use default if not passed in
        if verbosity is None:
            self.verbosity = int(self.config["GLOBAL"]["default_test_verbosity"])
        else:
            self.verbosity = verbosity

        self.test_result_summary = None
        self.test_output_list = list()
        self.test_result_list = list()

    def __str__(self):
        return str( self.path )

    def find_test_src_files( self ):
        test_srcs = find_files( os.path.join( self.path, self.config["FILE_DEF_TEST_SOURCE"]["path"] ), self.config["FILE_DEF_TEST_SOURCE"]["glob"] )

        for file in test_srcs:
            self.test_src_paths.append( file )
            self.test_sources.append( TestSrc( file ) )
        self.test_src_paths.sort()

    # Make sure this uses the test harness = UNITY config
    def find_tests_and_groups(self):
        # Find tests and groups for each test source file in the module
        # Add test groups to module attributes
        [src.getTestGroups() for src in self.test_sources]
        self.test_groups = [group for src in self.test_sources for group in src.TestGroups ]
        # [print(group.name) for group in self.test_groups]

    # This should grab a generator class and look for file defs in the "runner" category
    def gen_test_runner( self ):
        module_definition = self.config["GLOBAL"]["default_module_def"]
        hook_source = os.path.splitext( os.path.normpath( self.config[ module_definition ][ "file_gen_callbacks" ] ) )[0]
        hooks = __import__( hook_source, globals(), locals(), [], 0 )
        test_runner_generator = GeneratedFileDescriptor( self.name, self.config[ "CMOD_FILE_GENERATORS" ]["runner"], self.config, hooks )
        test_runner_generator.gen_file( self.path, self.config, self.test_groups )

    def run_makefile( self ):
        p1 = subprocess.Popen( ['make', '--directory', self.path ], stdout=subprocess.PIPE )
        p1.wait()

    def get_test_results( self ):
        result_files = find_files( os.path.join( self.path, self.config["FILE_DEF_TEST_RESULT"]["path"] ), self.config["FILE_DEF_TEST_RESULT"]["glob"] )

        if len( result_files ) == 0:
            print("More than one result files found:", result_files )
            sys.exit()
        if len( result_files ) > 1:
            print("More than one result files found:", result_files )
            sys.exit()
        test_output = UnityOutput( result_files[0] )
        self.test_output_list, self.test_result_summary = test_output.read_test_output()

        # Make an ordered list of test result objects
        # Each test case in the module,
        # Ask if it's name appears in any of the names in the TestResult list
        # If it does append a copy of the object to the results list
        # If not, append a default/passed TestResult obj to the list with that test's name
        test_case_list = list()
        lst = list()

        for source in self.test_sources:
            for group in source.TestGroups:
                for test in group.testList:
                    test_case_list.append( test )
                    lst.append( TestResult( source_file=str(source).strip(), test_group=str(group.name).strip(), test_case=str(test).strip(), result='PASS' ) )
        # [print(case) for case in lst]

        # Get a list of the tests that were mentioned in the Unity output
        mentioned_tests = list()
        for test_output in [case.test_case for case in self.test_output_list]:
            mentioned_tests.append( test_output )

        # Now we fill in the results list by iterating through the first list
        # lst = [TestResult() for i in range(len(test_case_list))]
        index = 0
        for test in test_case_list:
            if test in  mentioned_tests:
                obj_idx = mentioned_tests.index(test)
                lst[index] = self.test_output_list[obj_idx]
            index += 1
        self.test_result_list = lst
        # [print(case) for case in lst]

    def calculate_test_results( self ):
        pass

    def get_test_num_passed( self ):
        return self.test_result_summary.passed

    def get_test_num_failed( self ):
        return self.test_result_summary.failed

    def get_test_num_ignored( self ):
        return self.test_result_summary.ignored

    def get_test_num_total( self ):
        return self.test_result_summary.total

    def print_test_results( self, verbosity=None ):
        if verbosity is None:
            verbosity = self.verbosity

        if verbosity <= 2:
            return
        if( verbosity >= 7 ):
            print("")
            for source in self.test_sources:
                print(os.path.basename(source.path)+":")
                for group in source.TestGroups:
                    print("  "+group.name+":")
                    for test in group.testList:
                        for result in self.test_result_list:
                            # [print(result)]
                            # print(test, result.test_case, test==result.test_case)
                            # TODO: fix source file names not being equal
                            # if(test == result.test_case and group.name == result.test_group and source.path == result.source_file):
                            if(test == result.test_case and group.name == result.test_group):
                                print( result )
                            # print( source.path, result.source_file, (source.path == result.source_file) )
                            # print( group.name, result.test_group, (group.name == result.test_group) )
                            # print( test, result.test_case, (test == result.test_case) )
                print("")
            return
        elif( verbosity == 6 ):
            print("")
            for source in self.test_sources:
                for group in source.TestGroups:
                    print("  "+group.name+":")
                    for test in group.testList:
                        for result in self.test_result_list:
                            # [print(result)]
                            # print(test, result.test_case, test==result.test_case)
                            # TODO: fix source file names not being equal
                            # if(test == result.test_case and group.name == result.test_group and source.path == result.source_file):
                            if(test == result.test_case and group.name == result.test_group):
                                print( result )
                            # print( source.path, result.source_file, (source.path == result.source_file) )
                            # print( group.name, result.test_group, (group.name == result.test_group) )
                            # print( test, result.test_case, (test == result.test_case) )
                print("")
            return
        elif( verbosity == 5 ):
            print("")
            for result in self.test_result_list:
                print( result )
            print("")
            return
        elif verbosity == 4 and ( self.test_result_summary.failed > 0 or self.test_result_summary.ignored > 0 ):
            print("")
            for result in self.test_result_list:
                if result.result == 'FAIL' or result.result == 'IGNORE':
                    print( result )
            print("")
        elif verbosity == 3 and self.test_result_summary.failed > 0:
            print("")
            for result in self.test_result_list:
                if result.result == 'FAIL':
                    print( result )
            print("")

    def run_tests( self ):
        self.run_makefile()
        self.get_test_results()
        self.print_test_results()

