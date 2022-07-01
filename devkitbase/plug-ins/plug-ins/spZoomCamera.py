from __future__ import division

"""
reference: https://help.autodesk.com/view/MAYAUL/2022/ENU/?guid=Maya_SDK_py_ref_python_2api1_2py1_zoom_camera_cmd_8py_example_html
Usage - Zoom in the camera by twice the distance
Prereq - Create an object in the scene, add camera pointing to the object. 

"""

import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaMPx as OpenMayaMPx

"""
import maya.cmds as cmds
cmds.loadPlugin("zoomCameraCmd.py")
cmds.spZoomCamera() 

"""

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
            sys.stderr.write("ERROR: getting camera \n")
        else:
            self.redoIt()

    def isUndoable(self):
        return True

    # Cmd Creator
    def cmdCreator():
        return OpenMayaMPx.asMPxPtr(scriptedCommand())


# Initialize the script plug-in
def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.registerCommand(kPluginCmdName, scriptedCommand.cmdCreator)
    except:
        sys.stderr.write("Failed to register command: %s\n" % kPluginCmdName)


# Uninitialize the script plug-in
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterCommand(kPluginCmdName)
    except:
        sys.stderr.write("Failed to unregister command: %s\n" % kPluginCmdName)
