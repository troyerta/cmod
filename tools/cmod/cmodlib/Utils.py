import sys
import os
import re

def find_module_dir( module ):
    matches = list()
    # script = os.path.join( os.path.normpath(module), 'test' )
    # if os.path.isfile(script):
    test_dir = os.path.join( os.path.normpath(module), 'unit_testing' )
    if os.path.isdir(test_dir):
        matches.append( test_dir )
    return matches

def find_module_dirs_recursive( module ):
    pattern = "^unit_testing$"
    matches = list()
    for root, dirs, files in os.walk( module ):
        [matches.append( os.path.join(root, dir) ) for dir in filter(lambda x: re.match(pattern, x), dirs)]
    return matches

def find_modules( root_dir, recurse ):
    matches = list()
    if recurse is True:
        matches = find_module_dirs_recursive( root_dir )
    else:
        matches = find_module_dir( root_dir )
    return matches
