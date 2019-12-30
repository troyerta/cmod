import os
import errno
import sys

sys.path.insert(1, '../')

from Utils import get_date_str, splitpath

def gen_basename_src( path ):
    path_parts = splitpath(path)
    filename = path_parts[0].lower()
    if len(path_parts) > 1:
        for part in path_parts[1:]:
            filename += "_" + part.lower()
    filename += ".c"
    return filename

def gen_path_src( module_dir, mod_config ):
    return os.path.normpath( os.path.join( module_dir, mod_config["src_dir"], gen_basename_src( module_dir ) ) )

def print_section_header( file, name ):
    file.write('/**********************************************************\n')
    file.write('| '+name+'\n')
    file.write('**********************************************************/\n')

def print_included_headers( file, includes ):
    if includes != None:
        for each in includes:
            file.write('#include \"' + each + '\"\n')

def print_src( module_path, module_configs, global_configs ):
    # print("Test Source Gen")
    # print("\tfile_path =", file_path)
    # print("\ttarget_file =", basename)
    # print("\tdate =", date)
    # print("\tconfigs =", configs)
    # print("\tincludes =", includes)

    date = get_date_str()
    # config_obj = Config()
    # configs = config_obj.get_section_items('GLOBAL')
    file_path = gen_path_src( module_path, module_configs )

    basename = os.path.basename( file_path )
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w+") as f:
        f.write('/**********************************************************\n')
        f.write('| '+global_configs["project"]+' - '+basename+' \n')
        f.write('| Author: '+global_configs["author"]+'\n')
        f.write('| Date: '+date+'\n')
        f.write('| License: '+global_configs["license"]+'\n')
        f.write('| Repository: '+global_configs["repo"]+'\n')
        f.write('| Description:\n')
        f.write('**********************************************************/\n')
        f.write('\n')
        # print_section_header(f,'Includes')
        # print_included_headers(f, includes)
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