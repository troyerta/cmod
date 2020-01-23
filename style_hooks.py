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
    print( file_path )
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

def print_test_source( module_dir, configs ):
    print("Printing test source:")

def gen_test_source_pathname( module_dir, configs ):
    return "tests.c"

# runner

def gen_test_runner_pathname( module_dir, configs ):
    basename = os.path.splitext( os.path.basename( module_dir ))
    test_runner_basename = configs["FILE_DEF_TEST_RUNNER"]["prefix"] + basename[0].lower() + configs["FILE_DEF_TEST_RUNNER"]["suffix"] +'.c'
    return test_runner_basename

def print_test_runner( module_dir, configs ):
    print("Printing test runner:")

# makefile

def gen_makefile_pathname( module_dir, configs ):
    return "Makefile"

def print_makefile( module_dir, configs ):
    print("Printing makefile:")

# script

def gen_test_script_pathname( module_dir, configs ):
    return "test"

def print_test_script( module_dir, configs ):
    print("Printing test script:")
