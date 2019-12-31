import os
import sys

sys.path.insert(1, '../')

from Utils import get_date_str, splitpath

def gen_basename_hdr( path ):
    path_parts = splitpath(path)

    if len(path_parts) > 1:
        filename = path_parts[-1].lower()
    else:
        filename = path_parts[0].lower()
    filename += ".h"
    return filename

def gen_path_hdr( module_dir, mod_config ):
    norm_dir = os.path.normpath( module_dir )
    return os.path.normpath( os.path.join( mod_config["src_dir"], gen_basename_hdr( norm_dir ) ) )

def gen_basename_test_src( path ):
	path_parts = splitpath(path)
	filename = "test_" + path_parts[-1].lower() + "_tests.c"
	return filename

def gen_path_test_src( module_dir, mod_config ):
    norm_dir = os.path.normpath( module_dir )
    return os.path.normpath( os.path.join( norm_dir, mod_config["test_dir"], gen_basename_test_src( norm_dir ) ) )

def print_section_header( file, name ):
    file.write('/**********************************************************\n')
    file.write('| '+name+'\n')
    file.write('**********************************************************/\n')

def print_default_test_group_decl( file, group_name ):
    file.write('TEST_GROUP( ' + group_name + ' );\n')

def print_default_test_group_setup_decl( file, group_name ):
    file.write('TEST_SETUP( ' + group_name + ' )\n')
    file.write('{\n\n')
    file.write('}\n')

def print_default_test_group_teardown_decl( file, group_name ):
    file.write('TEST_TEAR_DOWN( ' + group_name + ' )\n')
    file.write('{\n\n')
    file.write('}\n')

def print_default_test_case( file, group_name ):
    file.write('TEST( ' + group_name + ', sampleTest )\n')
    file.write('{\n')
    file.write('TEST_IGNORE_MESSAGE( \"Tests for ' + group_name + ' are working\" );\n')
    file.write('}\n')

def print_include_potential_header( file, header_name ):
    file.write('// #include \"' + header_name + '\"\n')

def print_test_source( module_path, module_configs, global_configs ):
    date = get_date_str()
    file_path = gen_path_test_src( module_path, module_configs )
    header_include = gen_path_hdr( module_path, module_configs )
    print( file_path )
    basename = os.path.normpath( os.path.basename( file_path ) )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    project_name = global_configs["project"]
    author = global_configs["author"]
    license = global_configs["license"]
    repo = global_configs["repo"]
    test_group_name = os.path.basename(module_path.upper().strip("/"))+"_TEST_GROUP_A"

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
        print_include_potential_header(f, header_include)
        f.write('\n')
        print_section_header(f,'Test Groups')
        print_default_test_group_decl(f, test_group_name)
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
        print_default_test_group_setup_decl( f, test_group_name )
        f.write('\n')
        print_default_test_group_teardown_decl( f, test_group_name )
        f.write('\n')
        print_section_header(f,'Tests')
        print_default_test_case( f, test_group_name )
        f.close()