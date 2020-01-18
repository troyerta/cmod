import os
import sys

# src

def gen_source_name( module_dir, configs ):
    print("Gen source name")
    return "src.c"

def print_source( module_dir, configs ):
    print("Printing source")

# hdr

def gen_header_name( module_dir, configs ):
    print("Gen header name")
    return "hdr.h"

def print_header( module_dir, configs ):
    print("Printing header")

# test_src

def print_test_source( module_dir, configs ):
    print("Printing test source")

def gen_test_source_name( module_dir, configs ):
    pass

# runner

def gen_test_runner_name( module_dir, configs ):
    print("Gen runner name")
    basename = os.path.splitext( os.path.basename( module_dir ))
    test_runner_basename = configs["FILE_DEF_TEST_RUNNER"]["prefix"] + basename[0].lower() + self.config["FILE_DEF_TEST_RUNNER"]["suffix"] +'.c'
    return test_runner_basename

def print_test_runner( module_dir, configs ):
    print("Printing test runner")

# makefile

def gen_makefile_name( module_dir, configs ):
    print("Gen makefile name")
    return "Makefile"

def print_makefile( module_dir, configs ):
    print("Printing makefile")

# tester

def gen_test_script_name( module_dir, configs ):
    print("Gen test script name")
    return "src.c"

def print_test_script( module_dir, configs ):
    print("Printing test script")
