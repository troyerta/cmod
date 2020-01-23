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
    return module_dir

# header

def gen_header_basename( module_dir, configs ):
    return "hdr.h"

def print_header( module_dir, configs ):
    print("Printing header:")

# source

def gen_source_basename( module_dir, configs ):
    path_parts = splitpath( module_dir )

    if len(path_parts) > 1:
        filename = path_parts[-1].lower()
    else:
        filename = path_parts[0].lower()
    filename += ".c"

    return filename

def print_source( module_dir, configs ):
    print("Printing source:")
    date = get_date_str()
    file_path = os.path.join( module_name_callback( module_dir, configs ), \
        configs["FILE_DEF_SOURCE"]["path"], \
            gen_source_basename( module_dir, configs ) )
    file_path = os.path.normpath( file_path )
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

def gen_test_source_basename( module_dir, configs ):
    return "tests.c"

# runner

def gen_test_runner_basename( module_dir, configs ):
    basename = os.path.splitext( os.path.basename( module_dir ))
    test_runner_basename = configs["FILE_DEF_TEST_RUNNER"]["prefix"] + basename[0].lower() + configs["FILE_DEF_TEST_RUNNER"]["suffix"] +'.c'
    return test_runner_basename

def print_test_runner( module_dir, configs ):
    print("Printing test runner:")

# makefile

def gen_makefile_basename( module_dir, configs ):
    return "Makefile"

def print_makefile( module_dir, configs ):
    print("Printing makefile:")

# script

def gen_test_script_basename( module_dir, configs ):
    return "test"

def print_test_script( module_dir, configs ):
    print("Printing test script:")
