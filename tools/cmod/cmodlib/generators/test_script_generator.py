import os
import sys

sys.path.insert(1, '../')

from Utils import splitpath

def gen_path_test_script( module_dir, configs ):
    return os.path.join( module_dir, configs["FILE_DEF_TEST_SCRIPT"]["glob"] )

# def print_tdd_script( file_path, depth, module_config_tag ):
def print_test_script( module_dir, configs ):
    project_root_dir = '../'
    file_path = gen_path_test_script( module_dir, configs )

    depth = len( splitpath( file_path )) - 1
    for each in range(depth-1):
        project_root_dir = os.path.join( project_root_dir, '../' )

    env_path = os.path.join( project_root_dir, 'tools', 'cmod', 'venv', 'bin', 'python3' )

    os.makedirs(module_dir, exist_ok=True)

    with open(file_path, "w+") as f:
        f.write('#!' + env_path + '\n')
        f.write('\n')
        f.write('import sys\n')
        f.write('import subprocess\n')
        f.write('\n')
        f.write('module_path = \'' + module_dir + '\'\n')
        f.write('root_path = \'' + project_root_dir + '\'\n')
        f.write('\n')
        f.write('def main():\n')

        f.write('\tsubproc_cmd = [ \'./cmod\', \'test\', \'--m=\'+module_path ]\n\n')
        f.write('\tif len(sys.argv) > 1:\n')
        f.write('\t\t[subproc_cmd.append( arg ) for arg in sys.argv[1:]]\n')
        f.write('\tp1 = subprocess.Popen( subproc_cmd, cwd=root_path )\n')
        f.write('\tp1.wait()\n')
        f.write('\tsys.exit()\n')
        f.write('\n')
        f.write('if __name__ == \"__main__\":\n')
        f.write('\tmain()\n')
        f.close()

        os.chmod(file_path, 509)