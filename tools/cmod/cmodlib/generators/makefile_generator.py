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
        f.write( 'SRC_DIR = ' + configs["DEFAULT_MODULE_STRUCTURE"]['src_dir'] + '\n' )
        f.write( 'TEST_DIR = ' + configs["DEFAULT_MODULE_STRUCTURE"]['test_dir'] + '\n' )
        f.write( 'RUNNER_DIR = ' + configs["DEFAULT_MODULE_STRUCTURE"]['runner_dir'] + '\n' )
        f.write( 'OBJ_DIR = ' + configs["DEFAULT_MODULE_STRUCTURE"]['obj_dir'] + '\n' )
        f.write( 'ARTIFACTS_DIR = ' + configs["DEFAULT_MODULE_STRUCTURE"]['artifacts_dir'] + '\n' )
        f.write( 'EXE_DIR = ' + configs["DEFAULT_MODULE_STRUCTURE"]['exe_dir'] + '\n' )
        f.write( 'RESULTS_DIR = ' + configs["DEFAULT_MODULE_STRUCTURE"]['results_dir'] + '\n' )
        f.write( 'TEST_SRC_PREFIX = ' + configs["DEFAULT_MODULE_STRUCTURE"]['test_src_prefix'] + '\n' )
        f.write( 'TEST_SRC_SUFFIX = ' + configs["DEFAULT_MODULE_STRUCTURE"]['test_src_suffix'] + '\n' )
        f.write( 'RUNNER_SRC_PREFIX = ' + configs["DEFAULT_MODULE_STRUCTURE"]['runner_src_prefix'] + '\n' )
        f.write( 'RUNNER_SRC_SUFFIX = ' + configs["DEFAULT_MODULE_STRUCTURE"]['runner_src_suffix'] + '\n' )
        f.write( 'RESULTS_TXT_PREFIX = ' + configs["DEFAULT_MODULE_STRUCTURE"]['results_txt_prefix'] + '\n' )
        f.write( 'RESULTS_TXT_SUFFIX = ' + configs["DEFAULT_MODULE_STRUCTURE"]['results_txt_suffix'] + '\n' )
        f.write( 'include ' + template_path )
        f.write( '\n' )
        f.close()