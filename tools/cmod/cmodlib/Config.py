from configparser import SafeConfigParser
import sys
import os

# Perform checks on the required sections in the config.ini
# Make sure the minimally-required sections are present
# Make sure those sections have all the required options
'''
Make sure global settings section exists and has the
default_module_def option and the default test verbosity option

Make sure the value of default_module_def points to an existing section
Make sure that section has the two required options:
marker type and marker name

return the config parser if all is valid
'''

class Config:
    def __init__( self, config_file_path=None ):
        self.parser = SafeConfigParser()
        # self.config_dict = dict()
        if config_file_path == None:
            config_file_path = "config.ini"

        self.parser.read(config_file_path)

        # GLOBAL section must be present
        if not self.parser.has_section("GLOBAL"):
            print( config_file_path+':', "\'GLOBAL\' config section not found - exiting")
            sys.exit()

        # GLOBAL section must have default_module_def option
        if not self.parser.has_option( "GLOBAL", "default_module_def" ):
            print( config_file_path+':', "\'GLOBAL\' config section is missing required option \'default_module_def\' - exiting")
            sys.exit()

        # default_module_def option must exist as a section
        default_module_def = self.parser.get( "GLOBAL", "default_module_def" )
        if not self.parser.has_section( default_module_def ):
            print( config_file_path+':', "\'GLOBAL\' config option \'default_module_def\' specified section", "\'"+default_module_def+"\'", \
                "which was not found in", config_file_path, "- exiting")
            sys.exit()

        # default_module_def section must have a module_marker_type option
        if not self.parser.has_option( default_module_def, "module_marker_type" ):
            print( config_file_path+':', "section", "\'"+default_module_def+"\'",\
                 "must have option", "\'module_marker_type\'", "- exiting")
            sys.exit()

        # default_module_def section must be filled in
        if self.parser.get( default_module_def, "module_marker_type" ) == '':
            print( config_file_path+':', "section", "\'"+default_module_def+"\'", "option", "\'module_marker_type\':\
                 must be specified with \'directory\' or \'file\' setting - exiting")
            sys.exit()

        # default_module_def section must have a module_marker_name option
        if not self.parser.has_option( default_module_def, "module_marker_name" ):
            print( config_file_path+':', "section", "\'"+default_module_def+"\'", "must have option", "\'module_marker_name\'", "- exiting")
            sys.exit()

        # module_marker_name section must be filled in
        if self.parser.get( default_module_def, "module_marker_name" ) == '':
            print( config_file_path+':', "section", "\'"+default_module_def+"\'", "option", "\'module_marker_name\':", \
                "must be populated with a marker (file/dir) name - exiting")
            sys.exit()

    def get_parser(self):
        return self.parser
    # def get_configs(self):
    #     for section in self.parser.sections():
    #         self.config_dict[ section ] = self.get_section_items( section )
    #     return self.config_dict

    def get_all(self):
        for section_name in self.parser.sections():
            # print('Section:', section_name)
            # print('  Options:', self.parser.options(section_name))
            for name, value in self.parser.items(section_name):
                # print('  %s = %s' % (name, value))
                return

    def get_sections(self):
        for section_name in self.parser.sections():
            # print('Section:', section_name)
            return

    def get_section_options(self, section):
        # print('Section:', section)
        # print('  Options:', self.parser.options(section))
        return

    # Returns a dictionary of settings:values
    def get_section_items(self, section):
        name_list = []
        value_list = []
        # print('Section:', section)
        for name, value in self.parser.items(section):
            # print('  %s = %s' % (name, value))
            name_list.append(name)
            value_list.append(value)
        settings_dict = dict(zip(name_list, value_list))
        return settings_dict
