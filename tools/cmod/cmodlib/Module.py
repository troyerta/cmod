import os
import sys
import re
import subprocess

from Unity import TestSrc, TestResult, UnityOutput, TestSummary

class Module:
    def __init__( self, path, configs ):
        self.path = os.path.normpath( path )
        self.name = os.path.basename( self.path )
        self.config = configs
        self.test_sources = list()	# List of test source objects
        self.test_src_paths = list()	# list of paths
        self.test_groups = list()
        self.test_runner_path = None
        self.test_output_filepath = os.path.join( self.path, self.config["results_dir"], self.config["results_txt_prefix"] + self.name.lower() + self.config["results_txt_suffix"] + ".txt" )

        self.verbosity = int(self.config["default_verbosity"])
        self.test_result_summary = None
        self.test_output_list = list()
        self.test_result_list = list()

    def __str__(self):
        return str( self.path )

    def find_test_src_files( self ):
        find_test_src_regex = r'(?i)' + self.config["test_src_prefix"] + r'.*' + self.config["test_src_suffix"] + r'.c'
        files_and_dirs = os.listdir( os.path.join( self.path, self.config["test_dir"] ) )
        # print( files_and_dirs )
        test_srcs = list()

        for each in files_and_dirs:
            match = re.findall(find_test_src_regex, each)
            if match:
                test_srcs.append(match[0])
        for file in test_srcs:
            path = os.path.join( self.path, self.config["test_dir"], file )
            self.test_src_paths.append( path )
            self.test_sources.append( TestSrc( path ) )
        self.test_src_paths.sort()

    # Make sure this uses the test harness = UNITY config
    def find_tests_and_groups(self):
        # Find tests and groups for each test source file in the module
        # Add test groups to module attributes
        [src.getTestGroups() for src in self.test_sources]
        self.test_groups = [group for src in self.test_sources for group in src.TestGroups ]
        # [print(group.name) for group in self.test_groups]

    def gen_test_runner( self ):
        # For each test group object, make a call to it's runner in a new file
        basename = os.path.splitext( os.path.basename( self.path ))
        test_runner_basename = self.config["runner_src_prefix"] + basename[0].lower() + self.config["runner_src_suffix"] +'.c'
        self.test_runner_path = os.path.join( self.path, self.config["runner_dir"], test_runner_basename )
        os.makedirs( self.config["runner_dir"], exist_ok=True )
        # print( 'test_runner_basename =', test_runner_basename)

        with open(self.test_runner_path, "w+") as f:
            f.write('#include \"unity_fixture.h\"\n')
            f.write("\n")
            # Write out a Test Suite Runner for each suite
            # for test_src_obj in self.test_sources:
            for group in self.test_groups:
                f.write('TEST_GROUP_RUNNER( ' + group.name + ' )\n' )
                f.write('{\n')
                [f.write("RUN_TEST_CASE( " + group.name + ', ' + test_case + ' );\n') for test_case in group.testList]
                f.write('}\n\n')
            f.write("static void RunAllTests( void )\n")
            f.write("{\n")
            # for source in self.test_sources:
            for group in self.test_groups:
                f.write("RUN_TEST_GROUP( " + group.name + " );\n")
            f.write("}\n")
            f.write("\n")
            f.write("int main( int argc, const char * argv[] )\n")
            f.write("{\n")
            f.write("return UnityMain( argc, argv, RunAllTests );\n")
            f.write("}\n")
            f.write("\n")
            f.close()

    def run_makefile( self ):
        p1 = subprocess.Popen( ['make', '--directory', self.path ], stdout=subprocess.PIPE )
        p1.wait()

    def get_test_results( self ):
        test_output = UnityOutput( self.test_output_filepath )
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

    def print_test_results( self, verbosity=None ):
        if verbosity is None:
            verbosity = self.verbosity

        if verbosity <= 2:
            return

        if( verbosity >= 7 ):
            for source in self.test_sources:
                print(source.path+":")
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
