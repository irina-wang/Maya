import maya.cmds as cmds

from builtins import object
from maya import cmds
from maya import mel
from maya import OpenMaya as om
from maya import OpenMayaUI as omui 

from PySide2.QtCore import * 
from PySide2.QtGui import * 
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from shiboken2 import wrapInstance 

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin, MayaQWidgetDockableMixin
import functools


# for debug
# import pdb
# pdb.set_trace()


# placed in a 2D inactive overlay plane on the 3D viewport

#
# Define a procedure that returns a value to be used by the Heads Up Display
#
def objectPosition(*args):
	try:
		selectedNodes = cmds.selectedNodes()
		mainObj = selectedNodes[-1]
		positionList = cmds.getAttr('%s.translate' % mainObj)
		return positionList[0]
	except:
		return (0.0,0.0,0.0)

#
# Now, create a HUD object to display the return value of the above procedure
#
# Attributes:
#
#        - Section 1, block 0, represents the top second slot of the view.
#        - Set the blockSize to "medium", instead of the default "small"
#        - Assigned the HUD the label: "Position"
#        - Defined the label font size to be large
#        - Assigned the HUD a command to run on a SelectionChanged trigger
#        - Attached the attributeChange node change to the SelectionChanged trigger
#          to allow the update of the data on attribute changes.
#
a, b = cmds.headsUpDisplay( 'HUDObjectPosition', section=1, block=0, blockSize='medium', label='Position', labelFontSize='large', command=objectPosition, event='SelectionChanged', nodeChanges='attributeChange' )
print(a, b)

#
#Create a preset HUD object to display the camera names.
#
#Attributes:
#
#    - Section 2, block 0, represents the top middle slot of the view.
#    - Using blockalign, the HUD object is centered in the middle of the block
#    - Setting a dw of 50, allocates a space of 50 pixels for the data to reside in.
#    - Finally setting the preset to "cameraNames", selects a preset which will
#      automatically insert the associated data into the data field.
#

# display camera perspectives
cmds.headsUpDisplay('HUDCameraName', s=1, b=0, blockSize='medium', label='CameraName', labelFontSize='large', ba='center', dw=50 ,pre='cameraNames')

#
#Now, remove these two HUDs. Both can be removed in three ways: name, ID or position.
#The following examples will demonstrate removal by name and position
#
cmds.headsUpDisplay( 'HUDObjectPosition', rem=True )

# cmds.headsUpDisplay( rp=(7, 0) )
	