import sys
import maya.api.OpenMaya as OpenMaya

# ... additional imports here ...


##########################################################
# Plug-in
##########################################################
class MyCommandClass(OpenMaya.MPxCommand):
    kPluginCmdName = "myCommandName"

    def __init__(self):
        """Constructor."""
        OpenMaya.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        """Create an instance of our command."""
        return MyCommandClass()

    def doIt(self, args):
        """Command execution."""
        # Remove the following 'pass' keyword and replace it with
        # the code you want to run.
        pass


##########################################################
# Plug-in initialization.
##########################################################


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


def initializePlugin(mobject):
    """Initialize the plug-in when Maya loads it."""
    mplugin = OpenMaya.MFnPlugin(mobject)
    try:
        mplugin.registerCommand(
            MyCommandClass.kPluginCmdName, MyCommandClass.cmdCreator
        )
    except:
        sys.stderr.write("Failed to register command: " + MyCommandClass.kPluginCmdName)


def uninitializePlugin(mobject):
    """Uninitialize the plug-in when Maya un-loads it."""
    mplugin = OpenMaya.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(MyCommandClass.kPluginCmdName)
    except:
        sys.stderr.write(
            "Failed to unregister command: " + MyCommandClass.kPluginCmdName
        )


##########################################################
# Sample usage.
##########################################################
""" 
# Copy the following lines and run them in Maya's Python Script Editor:

import maya.cmds as cmds
cmds.loadPlugin('sampleCommand.py')
cmds.myCommandName()

"""
