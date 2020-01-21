import sys
import os
import pathlib

cmod_executable = r'cmod/venv/bin/python3.8'
cwd = os.getcwd()

help_types = [ '-h', '--h', 'help', '-help', '--help' ]

def find_cmod():
    # If help argument provided
    if len(sys.argv) == 1 or sys.argv[1] in help_types:
        print("User needs help")
        sys.exit()
    if not os.path.isfile("config.ini"):
        print( "config.ini missing or corrupted!")
        sys.exit()

    # Make sure the venv executable is running
    if not sys.executable.endswith( cmod_executable ):
        print("Not running the venv python")
        print( "Expected", cmod_executable )
        print("Found", sys.executable, "instead")
        sys.exit()
    return True

if find_cmod():
    sys.path.insert(0, 'tools/cmod/cmodlib')

if __name__ == "__main__":
    from Config import Config
    from ArgParse import ArgParser

    sys.path.insert( 0, os.getcwd() )

    # This a complete SafeConfigParser, so treat it nicely
    checked_configs = Config()
    configs = checked_configs.get_parser()

    cmod_arg_parser = ArgParser( sys.argv[1:], configs=configs )
    cmod_arg_parser.cmod_entry()