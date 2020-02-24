import os
import sys
from Utils import get_date_str, splitpath

# Reused functions

def print_section_header( file, name ):
    file.write('/**********************************************************\n')
    file.write('| '+name+'\n')
    file.write('**********************************************************/\n')

# module name

def module_name_callback( module_dir, configs ):
    return os.path.normpath( module_dir )

# header

def gen_header_pathname( module_dir, configs ):
    path_parts = splitpath( module_dir )

    if len(path_parts) > 1:
        filename = path_parts[-1].lower()
    else:
        filename = path_parts[0].lower()
    filename += ".h"
    filepath = os.path.normpath( os.path.join( module_name_callback( module_dir, configs ),\
        configs["FILE_DEF_HEADER"]["path"], \
            filename ) )
    return filepath

def print_header( module_dir, configs ):
    date = get_date_str()
    file_path = gen_header_pathname( module_dir, configs )
    basename = os.path.normpath( os.path.basename( file_path ) )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    project_name = configs["GLOBAL"]["project"]
    author       = configs["GLOBAL"]["author" ]
    license      = configs["GLOBAL"]["license"]
    repo         = configs["GLOBAL"]["repo"   ]

    include_guard = '_' + os.path.splitext(basename)[0].upper() + '_H_'

    with open(file_path, "w+") as f:
        f.write('/**********************************************************\n')
        f.write('| '+project_name+' - '+basename+' \n')
        f.write('| Author: '+author+'\n')
        f.write('| Date: '+date+'\n')
        f.write('| License: '+license+'\n')
        f.write('| Repository: '+repo+'\n')
        f.write('| Description:\n')
        f.write('**********************************************************/\n')
        f.write('\n')
        f.write('#ifndef ' + include_guard + '\n')
        f.write('#define ' + include_guard + '\n')
        f.write('\n')
        print_section_header(f,'Types')
        f.write('\n')
        print_section_header(f,'Literal Constants')
        f.write('\n')
        print_section_header(f,'Memory Constants')
        f.write('\n')
        print_section_header(f,'Variables')
        f.write('\n')
        print_section_header(f,'Macros')
        f.write('\n')
        print_section_header(f,'Public Function Prototypes')
        f.write('\n')
        f.write('#endif /* ' + include_guard + ' */\n')
        f.close()

# source

def gen_source_pathname( module_dir, configs ):
    path_parts = splitpath( module_dir )

    # Make the basename
    if len(path_parts) > 1:
        filepath = path_parts[-1].lower()
    else:
        filepath = path_parts[0].lower()
    filepath += ".c"

    # Use the module name callback and file descriptor path to get the full filepath
    filepath = os.path.join( module_name_callback( module_dir, configs ), \
        configs["FILE_DEF_SOURCE"]["path"], \
            filepath )
    filepath = os.path.normpath( filepath )
    return filepath

def print_source( module_dir, configs ):
    date = get_date_str()
    file_path = gen_source_pathname( module_dir, configs )
    # print( file_path )
    basename = os.path.normpath( os.path.basename( file_path ) )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    project_name = configs["GLOBAL"]["project"]
    author = configs["GLOBAL"]["author"]
    license = configs["GLOBAL"]["license"]
    repo = configs["GLOBAL"]["repo"]

    with open(file_path, "w+") as f:
        f.write('/**********************************************************\n')
        f.write('| '+project_name+' - '+basename+' \n')
        f.write('| Author: '+author+'\n')
        f.write('| Date: '+date+'\n')
        f.write('| License: '+license+'\n')
        f.write('| Repository: '+repo+'\n')
        f.write('| Description:\n')
        f.write('**********************************************************/\n')
        f.write('\n')
        print_section_header(f,'Includes')
        # print_include_potential_header(f, header_include)
        f.write('\n')
        print_section_header(f,'Types')
        f.write('\n')
        print_section_header(f,'Literal Constants')
        f.write('\n')
        print_section_header(f,'Memory Constants')
        f.write('\n')
        print_section_header(f,'Variables')
        f.write('\n')
        print_section_header(f,'Macros')
        f.write('\n')
        print_section_header(f,'Static Function Prototypes')
        f.write('\n')
        print_section_header(f,'Static Function Definitions')
        f.write('\n')
        print_section_header(f,'Function Definitions')
        f.close()

# test_source

#--------------------------------------
# Utility functions
#--------------------------------------
def print_section_header( file, name ):
    file.write('/**********************************************************\n')
    file.write('| '+name+'\n')
    file.write('**********************************************************/\n')

def print_unity_test_group_decl( file, group_name ):
    file.write('TEST_GROUP( ' + group_name + ' );\n')

def print_unity_test_group_setup_decl( file, group_name ):
    file.write('TEST_SETUP( ' + group_name + ' )\n')
    file.write('{\n\n')
    file.write('}\n')

def print_unity_test_group_teardown_decl( file, group_name ):
    file.write('TEST_TEAR_DOWN( ' + group_name + ' )\n')
    file.write('{\n\n')
    file.write('}\n')

def print_unity_test_case( file, group_name ):
    file.write('TEST( ' + group_name + ', sampleTest )\n')
    file.write('{\n')
    file.write('TEST_IGNORE_MESSAGE( \"Tests for ' + group_name + ' are working\" );\n')
    file.write('}\n')

def gen_test_source_pathname( module_dir, configs ):
    path_parts = splitpath( module_dir )
    basename = "test_" + path_parts[-1].lower() + "_tests.c"
    module = module_name_callback( module_dir, configs )
    full_path = os.path.join( module, configs["FILE_DEF_TEST_SOURCE"]["path"], basename )
    full_path = os.path.normpath( full_path )
    return full_path

def print_test_source( module_dir, configs ):
    date = get_date_str()
    file_path = gen_test_source_pathname( module_dir, configs )
    # header_include = gen_path_header( module_path, configs )
    # print( file_path )
    basename = os.path.normpath( os.path.basename( file_path ) )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    project_name = configs["GLOBAL"]["project"]
    author = configs["GLOBAL"]["author"]
    license = configs["GLOBAL"]["license"]
    repo = configs["GLOBAL"]["repo"]
    test_group_name = os.path.basename(module_name_callback( module_dir, configs ).upper().strip("/"))+"_TEST_GROUP_A"

    with open(file_path, "w+") as f:
        f.write('/**********************************************************\n')
        f.write('| '+project_name+' - '+basename+' \n')
        f.write('| Author: '+author+'\n')
        f.write('| Date: '+date+'\n')
        f.write('| License: '+license+'\n')
        f.write('| Repository: '+repo+'\n')
        f.write('| Description:\n')
        f.write('**********************************************************/\n')
        f.write('\n')
        print_section_header(f,'Includes')
        f.write("#include \"unity_fixture.h\"\n")
        # print_include_potential_header(f, header_include)
        f.write('\n')
        print_section_header(f,'Test Groups')
        print_unity_test_group_decl(f, test_group_name)
        f.write('\n')
        print_section_header(f,'Types')
        f.write('\n')
        print_section_header(f,'Literal Constants')
        f.write('\n')
        print_section_header(f,'Memory Constants')
        f.write('\n')
        print_section_header(f,'Variables')
        f.write('\n')
        print_section_header(f,'Macros')
        f.write('\n')
        print_section_header(f,'Test Setup and Teardown')
        print_unity_test_group_setup_decl( f, test_group_name )
        f.write('\n')
        print_unity_test_group_teardown_decl( f, test_group_name )
        f.write('\n')
        print_section_header(f,'Tests')
        print_unity_test_case( f, test_group_name )
        f.close()

# runner

def gen_test_runner_pathname( module_dir, configs ):
    basename = os.path.splitext( os.path.basename( module_dir ))
    test_runner_basename = configs["FILE_DEF_TEST_RUNNER"]["prefix"] + basename[0].lower() + configs["FILE_DEF_TEST_RUNNER"]["suffix"] +'.c'
    test_runner_pathname = os.path.join( module_dir, configs["FILE_DEF_TEST_RUNNER"]["path"], test_runner_basename )
    return test_runner_pathname

def print_test_runner( module_dir, configs, test_groups ):
    # print("Printing test runner:")

    test_runner_path = gen_test_runner_pathname( module_dir, configs )
    os.makedirs( os.path.join( module_dir, configs["FILE_DEF_TEST_RUNNER"]["path"]), exist_ok=True )
    with open(test_runner_path, "w+") as f:
        f.write('#include \"unity_fixture.h\"\n')
        f.write("\n")
        # Write out a Test Suite Runner for each suite
        for group in test_groups:
            f.write('TEST_GROUP_RUNNER( ' + group.name + ' )\n' )
            f.write('{\n')
            [f.write("RUN_TEST_CASE( " + group.name + ', ' + test_case + ' );\n') for test_case in group.testList]
            f.write('}\n\n')
        f.write("static void RunAllTests( void )\n")
        f.write("{\n")
        # for source in self.test_sources:
        for group in test_groups:
            f.write("RUN_TEST_GROUP( " + group.name + " );\n")
        f.write("}\n")
        f.write("\n")
        f.write("int main( int argc, const char * argv[] )\n")
        f.write("{\n")
        f.write("return UnityMain( argc, argv, RunAllTests );\n")
        f.write("}\n")
        f.write("\n")
        f.close()


# makefile

def gen_makefile_pathname( module_dir, configs ):
    return os.path.normpath( os.path.join( module_name_callback( module_dir, configs ), configs["FILE_DEF_SOURCE"]["path"], "Makefile" ) )

def print_makefile( module_dir, configs ):
    file_path = gen_makefile_pathname( module_dir, configs )
    # print( file_path )

    depth = len( splitpath( file_path )) - 1
    # print( depth )

    project_root_dir = '../'
    for each in range(depth-1):
        project_root_dir = os.path.join( project_root_dir, '../' )

    template_path = os.path.join( "$(PROJ_ROOT)", "unit_test", "module_makefile.mk" )
    # print("\ttemplate_path =", template_path)

    defaults_path = os.path.join( "$(PROJ_ROOT)", "unit_test", "module_defaults.mk" )
    # print("\tdefaults_path =", defaults_path)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w+") as f:
        f.write('\n')
        # Make this part test harness agnostic as well
        f.write( 'MODULE_DIR = ' + os.path.dirname( file_path ) + '\n' )
        f.write( 'PROJ_ROOT = ' + project_root_dir + '\n' )
        f.write( 'include ' + defaults_path + '\n' )
        f.write( 'include ' + template_path )
        f.write( '\n' )
        f.close()

# script

def gen_test_script_pathname( module_dir, configs ):
    return os.path.normpath( os.path.join( module_name_callback( module_dir, configs ), configs["FILE_DEF_SOURCE"]["path"], "test" ) )

def print_test_script( module_dir, configs ):
    project_root_dir = '../'
    file_path = gen_test_script_pathname( module_dir, configs )

    depth = len( splitpath( file_path )) - 1
    for each in range(depth-1):
        project_root_dir = os.path.join( project_root_dir, '../' )

    env_path = os.path.join( project_root_dir, 'tools', 'cmod', 'venv', 'bin', 'python3' )

    os.makedirs(module_dir, exist_ok=True)

    with open(file_path, "w+") as f:
        f.write('#!' + env_path + '\n')
        f.write('\n')
        f.write('import sys\n')
        f.write('import subprocess\n')
        f.write('\n')
        f.write('module_path = \'' + module_dir + '\'\n')
        f.write('root_path = \'' + project_root_dir + '\'\n')
        f.write('\n')
        f.write('def main():\n')

        f.write('\tsubproc_cmd = [ \'./cmod\', \'test\', \'--m=\'+module_path ]\n\n')
        f.write('\tif len(sys.argv) > 1:\n')
        f.write('\t\t[subproc_cmd.append( arg ) for arg in sys.argv[1:]]\n')
        f.write('\tp1 = subprocess.Popen( subproc_cmd, cwd=root_path )\n')
        f.write('\tp1.wait()\n')
        f.write('\tsys.exit()\n')
        f.write('\n')
        f.write('if __name__ == \"__main__\":\n')
        f.write('\tmain()\n')
        f.close()

        os.chmod(file_path, 509)
