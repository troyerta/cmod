import os
import sys

# Ask to overwrite the file if it already exists!

'''
Options as Flags:
parser = ConfigParser.SafeConfigParser(allow_no_value=True)
'''

def checkKey( key, dict ):
    if key not in dict:
        return False
    return True

def checkSectionExists( key, dict ):
    if checkKey( key, dict ) == False:
        print( "CMod config error: section", '\''+key+'\'', "could not be found in config.ini" )
        sys.exit()
    else:
        return key

def checkEntryExists( key, dict, section ):
    if checkKey( key, dict ) == False:
        print( "CMod config error: option", '\''+key+'\'', "could not be found in section", '\''+section+'\'' )
        sys.exit()
    else:
        return key

def checkEntryIsPopulated( key, dict, section ):
    if dict[key] == '':
        print( "CMod config error: option", '\''+key+'\'', "in section", '\''+section+'\'', "is without a value" )
        sys.exit()
    else:
        return key

def checkEntryExistsAndPopulated( key, dict, section ):
    temp1 = checkEntryExists( key, dict, section )
    temp2 = checkEntryIsPopulated( temp1, dict, section )
    return temp2

class FileDescriptor:
    def __init__( self, module, config_section, configs ):
        self.config_section = checkSectionExists( config_section, configs )
        self.path = checkEntryExistsAndPopulated( "path", configs[ self.config_section ], self.config_section )
        self.glob = checkEntryExistsAndPopulated( "glob", configs[ self.config_section ], self.config_section )

class GeneratedFileDescriptor( FileDescriptor ):
    def __init__( self, module, config_section, configs, hooks ):
        super().__init__( module, config_section, configs )
        self.name_gen_key = checkEntryExistsAndPopulated( "name_callback", configs[self.config_section], self.config_section )
        self.file_gen_key = checkEntryExistsAndPopulated( "generate_callback", configs[self.config_section], self.config_section )

        self.name_gen_callback_name = configs[ self.config_section ][self.name_gen_key]
        self.file_gen_callback_name = configs[ self.config_section ][self.file_gen_key]

        self.hooks = hooks

        self.gen_name = self.check_callback( self.hooks, self.name_gen_callback_name )
        self.gen_file = self.check_callback( self.hooks, self.file_gen_callback_name )

        self.filename = None

    # Returns the callback if valid
    def check_callback( self, hooks, callback_name ):
        if not callback_name:
            print( "callback not found in config" )
            sys.exit()
        if not hasattr( hooks, callback_name ):
            print( "callback", "\'"+callback_name+"\'", "in config could not be found in", hooks )
            sys.exit()
        callback = getattr( hooks, callback_name )
        if not callable( callback ):
            print( "callback", "\'"+callback_name+"\'", "is not callable from", hooks )
            sys.exit()
        return callback

class BuildArtifactFileDescriptor( FileDescriptor ):
    def __init__( self, module, config_section, configs, hooks ):
        super().__init__( module, config_section, configs, hooks )

        # More complex checking logic here since only one of these fields is required to even be present and populated
        self.prefix = configs[self.config_section]["prefix"]
        self.suffix = configs[self.config_section]["suffix"]
