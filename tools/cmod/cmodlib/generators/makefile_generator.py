import os
import sys

sys.path.insert(1, '../')

from Utils import splitpath

def gen_path_makefile( module_dir, configs ):
    return os.path.join( module_dir, "Makefile" )

# def print_makefile( file_path, depth, module_config_tag ):
def print_makefile( module_path, configs ):
    file_path = gen_path_makefile( module_path, configs )
    # print( file_path )

    depth = len( splitpath( file_path )) - 1
    # print( depth )

    project_root_dir = '../'
    for each in range(depth-1):
        project_root_dir = os.path.join( project_root_dir, '../' )

    template_path = os.path.join( "$(PROJ_ROOT)", "unit_test", "module_makefile" )
    # print("\ttemplate_path =", template_path)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w+") as f:
        f.write('\n')
        # Make this part test harness agnostic as well
        f.write( 'MODULE_DIR = ' + os.path.dirname( file_path ) + '\n' )
        f.write( 'PROJ_ROOT = ' + project_root_dir + '\n' )
        f.write( 'SRC_DIR = ' + configs["FILE_DEF_SOURCE"]['path'] + '\n' )
        f.write( 'HDR_DIR = ' + configs["FILE_DEF_HEADER"]['path'] + '\n' )
        f.write( 'TESTS_DIR = ' + configs["FILE_DEF_TEST_SOURCE"]['path'] + '\n' )
        f.write( 'RUNNER_DIR = ' + configs["FILE_DEF_TEST_RUNNER"]['path'] + '\n' )
        f.write( 'EXE_DIR = ' + configs["FILE_DEF_TEST_BUILD"]['path'] + '\n' )
        f.write( 'RESULTS_DIR = ' + configs["FILE_DEF_TEST_RESULT"]['path'] + '\n' )
        f.write( 'RESULTS_TXT_PREFIX = ' + configs["FILE_DEF_TEST_RESULT"]['prefix'] + '\n' )
        f.write( 'RESULTS_TXT_SUFFIX = ' + configs["FILE_DEF_TEST_RESULT"]['suffix'] + '\n' )
        f.write( 'include ' + template_path )
        f.write( '\n' )
        f.close()