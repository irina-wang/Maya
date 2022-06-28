import sys

import maya.api.OpenMaya as OpenMaya
# ... additional imports here ...

kPluginCmdName = 'myCommandWithFlag'

'''
Naming convention
starts with dash (-)
'''
kShortFlagName = '-mf'
kLongFlagName = '-myFlag'

def maya_useNewAPI():
	"""
	The presence of this function tells Maya that the plugin produces, and
	expects to be passed, objects created using the Maya Python API 2.0.
	"""
	pass
	
##########################################################
# Plug-in 
##########################################################
class MyCommandWithFlagClass( OpenMaya.MPxCommand ):
    
    def __init__(self):
        ''' Constructor. '''
        OpenMaya.MPxCommand.__init__(self)
    
    def doIt(self, args):
        ''' Command execution. '''
        
        # We recommend parsing your arguments first.
        self.parseArguments( args )

        # Remove the following 'pass' keyword and replace it with the code you want to run. 
        pass
    
    def parseArguments(self, args):
        ''' 
        The presence of this function is not enforced,
        but helps separate argument parsing code from other
        command code. 
        '''
        
        # The following MArgParser object allows you to check if specific flags are set.
        argData = OpenMaya.MArgParser( self.syntax(), args )
        
        if argData.isFlagSet( kShortFlagName ):
                
            # In this case, we print the passed flag's value as an integer.
            # We use the '0' to index the flag's first and only parameter.
            flagValue = argData.flagArgumentInt( kShortFlagName, 0 )
            print(kLongFlagName + ': ' + str( flagValue ))
            
        
        # ... If there are more flags, process them here ...

##########################################################
# Plug-in initialization.
##########################################################
def cmdCreator():
    ''' Create an instance of our command. '''
    return MyCommandWithFlagClass() 

def syntaxCreator():
    ''' Defines the argument and flag syntax for this command. '''
    syntax = OpenMaya.MSyntax()
    
    # In this example, our flag will be expecting a numeric value, denoted by OpenMaya.MSyntax.kDouble. 
    syntax.addFlag( kShortFlagName, kLongFlagName, OpenMaya.MSyntax.kDouble )
    
    # ... Add more flags here ...
        
    return syntax
    
def initializePlugin( mobject ):
    ''' Initialize the plug-in when Maya loads it. '''
    mplugin = OpenMaya.MFnPlugin( mobject )
    try:
        mplugin.registerCommand( kPluginCmdName, cmdCreator, syntaxCreator )
    except:
        sys.stderr.write( 'Failed to register command: ' + kPluginCmdName )

def uninitializePlugin( mobject ):
    ''' Uninitialize the plug-in when Maya un-loads it. '''
    mplugin = OpenMaya.MFnPlugin( mobject )
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( 'Failed to unregister command: ' + kPluginCmdName )

##########################################################
# Sample usage.
##########################################################
''' 
# Copy the following lines and run them in Maya's Python Script Editor:

import maya.cmds as cmds
cmds.loadPlugin( 'sampleCommandFlag.py' )
cmds.myCommandWithFlag( myFlag = 4 )

'''