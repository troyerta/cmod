import os
import sys

sys.path.insert(1, '../')

from Utils import splitpath

# def print_makefile( file_path, depth, module_config_tag ):
def print_makefile( module_path, module_configs, global_configs ):
    # print("Module Makefile Gen")
    # print("\tfile_path =", file_path)
    # print("\tdepth =", depth)
    file_path = os.path.join( module_path, "Makefile" )
    print( file_path )

    # TODO: Try me!
    depth = len( splitpath( file_path )) - 1
    print( depth )

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
        f.write( 'SRC_DIR = ' + module_configs['src_dir'] + '\n' )
        f.write( 'TEST_DIR = ' + module_configs['test_dir'] + '\n' )
        f.write( 'RUNNER_DIR = ' + module_configs['runner_dir'] + '\n' )
        f.write( 'OBJ_DIR = ' + module_configs['obj_dir'] + '\n' )
        f.write( 'ARTIFACTS_DIR = ' + module_configs['artifacts_dir'] + '\n' )
        f.write( 'EXE_DIR = ' + module_configs['exe_dir'] + '\n' )
        f.write( 'RESULTS_DIR = ' + module_configs['results_dir'] + '\n' )
        f.write( 'TEST_SRC_PREFIX = ' + module_configs['test_src_prefix'] + '\n' )
        f.write( 'TEST_SRC_SUFFIX = ' + module_configs['test_src_suffix'] + '\n' )
        f.write( 'RUNNER_SRC_PREFIX = ' + module_configs['runner_src_prefix'] + '\n' )
        f.write( 'RUNNER_SRC_SUFFIX = ' + module_configs['runner_src_suffix'] + '\n' )
        f.write( 'RESULTS_TXT_PREFIX = ' + module_configs['results_txt_prefix'] + '\n' )
        f.write( 'RESULTS_TXT_SUFFIX = ' + module_configs['results_txt_suffix'] + '\n' )
        f.write( 'include ' + template_path )
        f.write( '\n' )
        f.close()