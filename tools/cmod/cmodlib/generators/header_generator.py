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

def gen_path_header( module_dir, mod_config ):
    norm_dir = os.path.normpath( module_dir )
    return os.path.normpath( os.path.join( norm_dir, mod_config["src_dir"], gen_basename_hdr( norm_dir ) ) )

def print_section_header( file, name ):
    file.write('/**********************************************************\n')
    file.write('| '+name+'\n')
    file.write('**********************************************************/\n')

def print_included_headers( file, includes ):
    if includes != None:
        for each in includes:
            file.write('#include \"' + each + '\"\n')

def print_header( module_path, module_configs, global_configs ):
    date = get_date_str()
    file_path = gen_path_header( module_path, module_configs )
    # print( file_path )
    basename = os.path.normpath( os.path.basename( file_path ) )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    project_name = global_configs["project"]
    author       = global_configs["author" ]
    license      = global_configs["license"]
    repo         = global_configs["repo"   ]

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
