import os
import sys
import re
import subprocess

from Unity import TestSrc

class Module:
    def __init__( self, path, configs ):
        self.path = os.path.normpath( path )
        self.name = os.path.basename( self.path )
        self.test_sources = list()	# List of test source objects
        self.config = configs
        self.test_src_paths = list()	# list of paths
        self.test_groups = list()

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
        test_runner_path = os.path.join( self.path, self.config["runner_dir"], test_runner_basename )
        os.makedirs( self.config["runner_dir"], exist_ok=True )
        # print( 'test_runner_basename =', test_runner_basename)

        with open(test_runner_path, "w+") as f:
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

    def read_test_output( self ):
        print("reading test output")

    def print_test_results( self ):
        print("printing test result")

    def run_tests( self ):
        self.run_makefile()
        self.read_test_output()
        self.print_test_results()
