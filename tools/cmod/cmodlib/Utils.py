import sys
import os
import re
import datetime

def find_module_dir( module, marker_type, marker_name ):
    matches = list()
    # script = os.path.join( os.path.normpath(module), 'test' )
    # if os.path.isfile(script):
    test_marker = os.path.join( os.path.normpath(module), marker_name )

    if marker_type == "file" and os.path.isfile( test_marker ):
            matches.append( test_marker )
    elif os.path.isdir( test_marker ):
            matches.append( test_marker )
    return matches

def find_module_dirs_recursive( module, marker_type, marker_name ):
    pattern = "^" + marker_name + "$"
    matches = list()

    if marker_type == "file":
        for root, dirs, files in os.walk( module ):
            [matches.append( os.path.join(root, fil) ) for fil in filter(lambda x: re.match(pattern, x), files)]
    else:
        for root, dirs, files in os.walk( module ):
            [matches.append( os.path.join(root, dir) ) for dir in filter(lambda x: re.match(pattern, x), dirs)]
    return matches

def find_modules( root_dir, recurse, configs ):
    matches = list()

    marker_type = configs["DEFAULT_MODULE_STRUCTURE"]["module_marker_type"]
    marker_name = configs["DEFAULT_MODULE_STRUCTURE"]["module_marker_name"]

    # Check for valid config.ini marker settings
    if marker_type != "directory" and marker_type != "file":
        print("Invalid marker type in config.ini\nPlease use \'directory\' or \'file\'")
        sys.exit()

    if recurse is True:
        matches = find_module_dirs_recursive( root_dir, marker_type, marker_name )
    else:
        matches = find_module_dir( root_dir, marker_type, marker_name )
    return matches

def get_date_str():
    date_time = datetime.datetime.now()
    date_time_str = date_time.strftime("%Y-%m-%d %H:%M")
    date_str = date_time_str.split(' ',1)
    return date_str[0]

def splitpath(path, maxdepth=20):
     ( head, tail ) = os.path.split(path)
     return splitpath(head, maxdepth - 1) + [ tail ] \
         if maxdepth and head and head != path \
         else [ head or tail ]
