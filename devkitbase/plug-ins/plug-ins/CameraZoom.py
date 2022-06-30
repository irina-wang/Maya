from __future__ import division

import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaMPx as OpenMayaMPx

kPluginCmdName = "spZoomCamera"

print("zoomCameraCmd.py has been imported....")

# command
class scriptedCommand(OpenMayaMPx.MPxCommand):
    camera = OpenMaya.MDagPath()
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    def redoIt(self):
        global camera
        fnCamera = OpenMaya.MFnCamera(camera)
        f1 = fnCamera.focalLength()
        fnCamera.setFocalLength(f1 * 2.0)

    def undoIt(self):
        global camera
        fnCamera = OpenMaya.MFnCamera(camera)
        f1 = fnCamera.focalLength()
        fnCamera.setFocalLength(f1 / 2.0)

    def doIt(self, args):
        global camera
        camera = OpenMaya.MDagPath()    
        try:
            OpenMayaUI.M3dView.active3dView().getCamera(camera)
        except: 
            sys.stderr.write( "ERROR: getting camera \n" )
        else:
            self.redoIt()

    def isUndoable(self):
        return True

# Cmd Creator
    def cmdCreator():
        return OpenMayaMPx.asMPxPtr(scriptedCommand() )
       
# Initialize the script plug-in 
    def initializePlugin(obj):
        plugin = OpenMaya.MFnPlugin(obj)
        try:
            plugin.registerCommand(kPluginCmdName, scriptedCommand.cmdCreator)
        except:
            sys.stderr.write("Failed to register command: %s\n" % kPluginCmdName )

# Uninitialize the script plug-in   
    def uninitializePlugin(obj):
        plugin = OpenMaya.MFnPlugin(obj)
        try:
            plugin.deregisterCommand(kPluginCmdName)        
        except:
            sys.stderr.write("Failed to unregister command: %s\n" % kPluginCmdName )