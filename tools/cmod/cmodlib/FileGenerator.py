import os
import sys

# Ask to overwrite the file if it already exists!

'''
SafeconfigParser useful methods:

has_section()

has_option()

Options as Flags:
parser = ConfigParser.SafeConfigParser(allow_no_value=True)



'''


def checkKey( key, dict ):
    if key not in dict:
        return False
    return True

def checkSectionExists( key, dict ):
    if checkKey( key, dict ) == False:
        print( '\''+key+'\'', "section not found in config.ini" )
        sys.exit()
    else:
        return key

def checkEntryExists( key, dict, section ):
    if checkKey( key, dict ) == False:
        print( '\''+key+'\'', "entry not found in", '\''+section+'\'' )
        sys.exit()
    else:
        return key

def checkEntryIsPopulated( key, dict, section ):
    if dict[key] == '':
        print( '\''+key+'\'', "in", section, "is without a value" )
        sys.exit()
    else:
        return key

def checkEntryExistsAndPopulated( key, dict, section ):
    temp = checkEntryExists( key, dict, section )
    temp = checkEntryIsPopulated( key, dict, section )
    return key

class FileDescriptor:
    def __init__( self, module, config_section, configs, hooks ):
        print("Making a FileGenerator class..")
        self.config_section = checkSectionExists( config_section, configs )

        self.path = checkEntryExistsAndPopulated( "path", configs[ self.config_section ], self.config_section )
        self.glob = checkEntryExistsAndPopulated( "glob", configs[ self.config_section ], self.config_section )
        self.hooks = hooks

class GeneratedFileDescriptor( FileDescriptor ):
    def __init__( self, module, config_section, configs, hooks ):
        super.__init__( module, config_section, configs, hooks )
        self.name_gen_callback = checkEntryExistsAndPopulated( "name_callback", configs[self.config_section], self.config_section )
        self.file_gen_callback = checkEntryExistsAndPopulated( "generate_callback", configs[self.config_section], self.config_section )

class BuildArtifactFileDescriptor( FileDescriptor ):
    def __init__( self, module, config_section, configs, hooks ):
        super.__init__( module, config_section, configs, hooks )

        # More complex checking logic here since only one of these fields is required to even be present and populated
        self.prefix = configs[self.config_section]["prefix"]
        self.suffix = configs[self.config_section]["suffix"]

    # def check( self ):
    #     pass

    # def check_configs( self ):
    #     pass

    # def get_config_status( self ):
    #     pass

    # def get_name_callback_status( self ):
    #     pass

    # def get_print_callback_status( self ):
    #     pass

    # def get_status( self ):
    #     pass

    # def test_name_callback( self ):
    #     pass

    # def test_print_callback( self ):
    #     pass
