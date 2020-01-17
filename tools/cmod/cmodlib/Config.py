from configparser import SafeConfigParser
import os

class Config:
    def __init__( self, config_file_path=None ):
        self.parser = SafeConfigParser()
        self.config_dict = dict()
        if config_file_path == None:
            self.parser.read("config.ini")
        else:
            self.parser.read(config_file_path)

    def get_configs(self):
        for section in self.parser.sections():
            self.config_dict[ section ] = self.get_section_items( section )
        return self.config_dict

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
