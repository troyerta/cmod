import os
import sys
import argparse
import re
from TaskQueue import run
from ProcQueue import multi_proc
import time

sys.path.insert(1, 'tools/cmod/cmodlib/generators')

# These are the different ways to invoke associated commands
help_types     = [ 'help', 'h', '-h', '--h', '--help' ]
generate_types = [ 'generate', 'gen' ]
clean_types    = [ 'clean' ]
list_types     = [ 'list', 'l' ]
tree_types     = [ 'tree', 'tr' ]
test_types     = [ 'test', 'tst', 'tdd', 'td' ]

cmd_string_list = [ \
    help_types, \
    generate_types, \
    clean_types, \
    list_types, \
    tree_types, \
    test_types \
    ]

# Store the available commands in a list, using the first elements from each action*_type list
action_types = [cmd_string_list[cmd_idx][0] for cmd_idx in range(len(cmd_string_list))]
# print( action_types )

# Command Strings
cmd_description_help     = "help command description"
cmd_description_generate = "generate command description"
cmd_description_clean    = "clean command description"
cmd_description_list     = "list command description"
cmd_description_tree     = "tree command description"
cmd_description_test     = "tdd command description"

cmd_description_msgs = [ \
    cmd_description_help, \
    cmd_description_generate, \
    cmd_description_clean, \
    cmd_description_list, \
    cmd_description_tree, \
    cmd_description_test \
    ]

cmd_usage_help     = "help command example"
cmd_usage_generate = "generate command example"
cmd_usage_clean    = "clean command example"
cmd_usage_list     = "list command example"
cmd_usage_tree     = "tree command example"
cmd_usage_test     = "tdd command example"

cmd_usage_msgs = [ \
    cmd_usage_help, \
    cmd_usage_generate, \
    cmd_usage_clean, \
    cmd_usage_list, \
    cmd_usage_tree, \
    cmd_usage_test \
    ]

cmd_help_help     = "help command help message"
cmd_help_generate = "generate command help message"
cmd_help_clean    = "clean command help message"
cmd_help_list     = "list command help message"
cmd_help_tree     = "tree command help message"
cmd_help_test     = "tdd command help message"

cmd_help_msgs = [ \
    cmd_help_help, \
    cmd_help_generate, \
    cmd_help_clean, \
    cmd_help_list, \
    cmd_help_tree, \
    cmd_help_test \
    ]

# Argument Strings
arg_help_module    = "How to use the module argument:"
arg_help_verbosity = "How to use the verbosity argument"
arg_help_types     = "How to use the types argument"
arg_help_recurse   = "How to use the --recurse flag"
arg_help_dry_run   = "How to use the --dry flag"
arg_help_runners   = "How to use the --runners flag"
arg_help_builds    = "How to use the --builds flag"
arg_help_results   = "How to use the --results flag"
arg_help_all       = "How to use the --all flag"
arg_help_venv      = "How to use the --venv flag"
arg_help_verbose   = "How to use the --verbose flag"
arg_help_suites    = "How to use the --suites flag"
arg_help_tests     = "How to use the --tests flag"
arg_help_scripts   = "How to use the --scripts flag"

# Argument "objects" is a reusable form
module_arg    = (('--module', '-module', '--m', '-m'),   {'dest':'module',    'help':arg_help_module,    'type':str,          })
mod_arg_reqd  = (('--module', '-module', '--m', '-m'),   {'dest':'module',    'help':arg_help_module,    'type':str, 'required':True })
verbosity_arg = (('--v', '-v'),                          {'dest':'verbosity', 'help':arg_help_verbosity, 'type':str,          })
types_arg     = (('--types', '-types', '--t', '-t'),     {'dest':'types',     'help':arg_help_types,     'type':str,          })
recurse_flag  = (('--r', '-r'),                          {'dest':'recurse',   'help':arg_help_recurse,   'action':'store_true'})
dry_run_flag  = (('--dry', '-dry', '--d', '-d'),         {'dest':'dry',       'help':arg_help_dry_run,   'action':'store_true'})
runners_flag  = (('--runners', '-runners'),              {'dest':'runners',   'help':arg_help_runners,   'action':'store_true'})
builds_flag   = (('--builds', '-builds'),                {'dest':'builds',    'help':arg_help_builds,    'action':'store_true'})
results_flag  = (('--results', '-results'),              {'dest':'results',   'help':arg_help_results,   'action':'store_true'})
all_flag      = (('--all', '-all'),                      {'dest':'all',       'help':arg_help_all,       'action':'store_true'})
venv_flag     = (('--venv', '-venv'),                    {'dest':'venv',      'help':arg_help_venv,      'action':'store_true'})
verbose_flag  = (('--verbose', '-verbose'),              {'dest':'verbose',   'help':arg_help_verbose,   'action':'store_true'})
suites_flag   = (('--suites', '-suites'),                {'dest':'suites',    'help':arg_help_suites,    'action':'store_true'})
tests_flag    = (('--tests', '-tests'),                  {'dest':'tests',     'help':arg_help_tests,     'action':'store_true'})
scripts_flag  = (('--scripts', '-scripts'),              {'dest':'scripts',   'help':arg_help_scripts,   'action':'store_true'})

# Set the parameters used by cmod commands
generate_args = [ \
    mod_arg_reqd, \
    types_arg \
    ]

workspace_args = [ \
    module_arg, \
    verbosity_arg, \
    recurse_flag \
    ]

tree_args = [ \
    module_arg, \
    suites_flag, \
    tests_flag \
    ]

cleaner_args = [ \
    module_arg, \
    recurse_flag, \
    dry_run_flag, \
    runners_flag, \
    builds_flag, \
    results_flag, \
    scripts_flag, \
    all_flag, \
    venv_flag, \
    verbose_flag
    ]

cmd_arg_types = [ \
    None, \
    generate_args, \
    cleaner_args, \
    workspace_args, \
    tree_args, \
    workspace_args \
    ]

def handle_help( args, configs ):
    print("handling help")

def get_generators( types ):
    gen_flags = list()
    if "c" in types:
        gen_flags.append( "source" )
    if "h" in types:
        gen_flags.append( "header" )
    if "t" in types:
        gen_flags.append( "test_source" )
    if "m" in types:
        gen_flags.append( "makefile" )
    if "s" in types:
        gen_flags.append( "script" )
    return gen_flags

def handle_generate( args, configs ):
    # From FileDef import FileDef
    # From Generator import Generator

    # try_to_import_hooks_module

    # # Look at the callback configs to determine if we have valid, callable functions

    # Print all configs to sanity check what we receive here
    # for section in configs.keys():
        # print(section)
        # for x in configs[section].keys():
            # print('    ', x, ':', configs[section][x])

    # We should not be directly using configs here... I think we should just
    # pass the configs to a file_def generator object which does all the validation checking
    # And generation or filepath preview strings
    # And then we should pass those file gen objects to a module generator object
    # Which should run the file generators

    hook_source = os.path.splitext( os.path.normpath( configs[configs["GLOBAL"]["default_module_def"]]["mod_callbacks"] ) )[0]
    print( hook_source )

    _hooks = __import__( hook_source, globals(), locals(), [], 0 )

    # Call the name callbacks to preview the full file path using
    # the configs[path_in_module] + '/' + configs[name_callback]

    from source_generator      import print_source, gen_path_src
    from header_generator      import print_header, gen_path_header
    from test_source_generator import print_test_source, gen_path_test_source
    from test_script_generator import print_test_script, gen_path_test_script
    from makefile_generator    import print_makefile, gen_path_makefile

    # Make sure raw path arg string has no leading slash
    module_dir = args.module.lstrip("/")
    # print( module_dir )

    # If user passed in specifc generator flags, handle those only
    # print( args.types )
    if args.types is not None:
        types = get_generators( args.types )
    else:
        # Set flags that generate a module, according to the module definition
        # specified by "default_module_def"
        types = [ key for key in list(configs[configs["GLOBAL"]["default_module_def"]].keys()) if key in list(configs["FILE_GENERATORS"].keys()) ]
    print('')

    # Get the file generators dict
    file_generators = configs["FILE_GENERATORS"]

    print(types)

    # List the FILE DEFs we will use - show user a preview of what will be made
    for key in file_generators.keys():
        if key in types:
            print("Would make a", key, "by using", file_generators[key], "FILE GENERATOR" )
            file_def_section = file_generators[key]

            name_cb = configs[file_def_section]["name_callback"]
            # attrs = dir(name_cb)
            # print(hasattr( name_cb, '__callable__' ))
            if name_cb:
                print("name callback found")
                if hasattr( _hooks, name_cb ):
                    print("obj found")
                    name_hook = getattr( _hooks, name_cb )
                    if callable(name_hook):
                        print( "callable!" )
                else:
                    print("obj not found")
            else:
                print("Not in config")
            # print_cb = configs[file_def_section]["generate_callback"]
            # if hasattr( _hooks, print_cb ):
                # printer_hook = getattr( _hooks, print_cb )

            # print( callable(name_hook) )
            # print( callable(printer_hook) )


    # print( types )
    print('')
    answer = input("Generate? Y/n: ")

    if answer != 'n':
        pass
    else:
        print("canceled")
        sys.exit()
    # print( args )


def handle_list( args, configs ):
    from Workspace import Workspace
    wksp = Workspace( args=args, configs=configs )
    wksp.print_module_names()

def handle_tree( args, configs ):
    from Tree import tree
    tree( args )

def handle_report( args, configs ):
    print("handling report\n")

def handle_stat( args, configs ):
    print("handling stat\n")

def handle_format( args, configs ):
    print("handling format\n")

def handle_analyze( args, configs ):
    print("handling analyze\n")

# Change this to a function that only operates on a
# single module
def handle_test( args, configs ):
    from Workspace import Workspace
    from Module import do_test_cycle
    wksp = Workspace( args, configs=configs )

    if wksp.num_modules > 20:
        from Module import do_test_cycle
        # Start a parallel process queue
        start = time.time()
        multi_proc( do_test_cycle, wksp.module_objs )
        print(f'Time taken = {time.time() - start:.2f}')
        # run( do_test_cycle, wksp.module_objs )
    else:
        # Runs tests with current process
        start = time.time()
        wksp.find_wksp_test_src_files()
        wksp.find_wksp_tests_and_groups()
        wksp.gen_wksp_test_runners()
        wksp.run_wksp_tests()
        wksp.calculate_test_result_totals()
        wksp.print_test_summary()
        print(f'Time taken = {time.time() - start:.10f}')

def handle_clean( args, configs ):
    from Clean import Cleaner
    cleaner = Cleaner( args, configs )
    cleaner.build_file_list()
    cleaner.do_cleaning()

action_handlers = [ \
    handle_help, \
    handle_generate, \
    handle_clean, \
    handle_list, \
    handle_tree,  \
    handle_test \
    ]

# Use the cmd index to lookup the cmd-associated data
cmd_handler_dict      = dict(zip(action_types, action_handlers))
cmd_args_dict         = dict(zip(action_types, cmd_arg_types))
cmd_descriptions_dict = dict(zip(action_types, cmd_description_msgs))
cmd_usage_msg_dict    = dict(zip(action_types, cmd_usage_msgs))
cmd_help_msg_dict     = dict(zip(action_types, cmd_help_msgs))

# TEST ME
def get_normalized_cmd( input_cmd ):
    idx = 0
    while input_cmd not in cmd_string_list[idx]:
        idx+=1
    # Return the first string - the full name of the command
    return cmd_string_list[idx][0]

def get_normalized_command( input_cmd ):
    if input_cmd in help_types:
        return action_types[0]
    elif input_cmd in generate_types:
        return action_types[1]
    elif input_cmd in clean_types:
        return action_types[2]
    elif input_cmd in list_types:
        return action_types[3]
    elif input_cmd in tree_types:
        return action_types[4]
    elif input_cmd in test_types:
        return action_types[5]
    else:
        print("invalid cmod command:", "\""+input_cmd+"\"" )
        sys.exit()

# This class collects everything needed for running cmod commands
class CmodCommand:
    def __init__( self, cmd ):
        self.handler = cmd_handler_dict[cmd]
        self.arg_types = cmd_args_dict[cmd]
        self.description = cmd_descriptions_dict[cmd]
        self.usage = cmd_usage_msg_dict[cmd]
        self.help_msg = cmd_help_msg_dict[cmd]
        self.arg_namespace = None

    # Produce a namespace variable with the argparser, given the passed-in arguments
    def get_arg_namespace( self, args ):
        parser = argparse.ArgumentParser( description=self.description, usage=self.usage )
        if self.arg_types is not None:
            [parser.add_argument( *arg[0], **arg[1] ) for arg in self.arg_types]

            # Consider passing the parser over tot he handler, so each command
            # can optionally add runtime-generated arguments - like clean's
            # ability to ID files to clean with flags generated from the config
            self.arg_namespace = parser.parse_args( args )

    # This where configs and arguments are passed to Cmod commands
    def run( self, configs ):
        self.handler( self.arg_namespace, configs )

# This class applies the passed arguments and configs to a cmod command, then runs it
class ArgParser:
    def __init__( self, sys_args=None, configs=None ):
        self.args = sys_args
        self.configs = configs

    # Get the intended command, setup the command to run, and run it
    def cmod_entry( self ):
        cmd = get_normalized_command( self.args[0] )
        self.args.remove( self.args[0] )
        command = CmodCommand( cmd )
        command.get_arg_namespace( self.args )
        command.run( self.configs )
        sys.exit()