import os
import sys

from Workspace import Workspace
from Module import Module
from Unity import TestSrc

class TestDrive:
    def __init__( self, args=None, global_cfg=None, mod_cfg=None ):
        self.args = args
        self.global_cfg = global_cfg
        self.mod_cfg = mod_cfg

    def run_cycle( self ):
        wksp = Workspace( self.args, mod_cfg=self.mod_cfg )
        wksp.find_wksp_test_src_files()
        wksp.find_wksp_tests_and_groups()
        wksp.gen_test_runners()
        wksp.run_tests()

        # Back to 1 process
        # wksp.print_test_summary()
