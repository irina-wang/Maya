from pydoc import visiblename
from re import L
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


def cameraName(*args):
	try:
		selectedNodes = cmds.selectedNodes()
		mainObj = selectedNodes[-1]
		print(mainObj[1:])
	except:
		print('Error: No object selected. ')


# cameraName()

cmds.headsUpDisplay('HUDName', section=1, block=0, blockSize='medium', label='Cam', labelFontSize='large', command=objectPosition, event='SelectionChanged', nodeChanges='attributeChange' )

def getTime(self):
	'''
	Get 
	'''
	try:
		selectedNodes = cmds.selectedNodes()
		mainObj = selectedNodes[-1]
		return mainObj[1:] # format the name 
	except:
		print('Error: No object selected. ')
		return ''


#
# Now, create a HUD object to display the return value of the above procedure
#
# Attributes:
#
#		- Section 1, block 0, represents the top second slot of the view.
#		- Set the blockSize to "medium", instead of the default "small"
#		- Assigned the HUD the label: "Position"
#		- Defined the label font size to be large
#		- Assigned the HUD a command to run on a SelectionChanged trigger
#		- Attached the attributeChange node change to the SelectionChanged trigger
#		  to allow the update of the data on attribute changes.
#
a, b = cmds.headsUpDisplay( 'HUDObjectPosition', section=1, block=0, blockSize='medium', label='Position', labelFontSize='large', command=objectPosition, event='SelectionChanged', nodeChanges='attributeChange' )
print(a, b)

#
#Create a preset HUD object to display the camera names.
#
#Attributes:
#
#	- Section 2, block 0, represents the top middle slot of the view.
#	- Using blockalign, the HUD object is centered in the middle of the block
#	- Setting a dw of 50, allocates a space of 50 pixels for the data to reside in.
#	- Finally setting the preset to "cameraNames", selects a preset which will
#	  automatically insert the associated data into the data field.
#

# display camera perspectives
cmds.headsUpDisplay('HUDCameraName', s=3, b=0, blockSize='medium', label='CameraName', labelFontSize='large', ba='center', dw=50 ,pre='cameraNames')

#
#Now, remove these two HUDs. Both can be removed in three ways: name, ID or position.
#The following examples will demonstrate removal by name and position
#
cmds.headsUpDisplay( 'HUDObjectPosition', rem=True )

# cmds.headsUpDisplay( rp=(7, 0) )
	

'''
Display button 

'''
import maya.cmds as cmds

# Define a "Hello!" counter procedure. This procedure will output
# "Hello! [number]"
# each time it is run. The number is incremented at the end of each call.
#
gHelloCount = 0
HUDID = 0

def HUDButtonReleased(*args):
	global HUDID, startTime
	if cmds.headsUpDisplay('HUDTime',section=1, b=6):
		cmds.headsUpDisplay('HUDTime', rem=True)
		HUDID = 0
	if not HUDID:
		print('start recording')
		# code that is being timed
		startTime = getStartTime()
		HUDID = cmds.headsUpDisplay('HUDTime', section=1, b=6, ba='left' , blockSize='medium', label='Start Recording', labelFontSize='large')
	else:
		print('end recording')
		totalTime = getEndTime(startTime)
		print('Total time: ', totalTime)
		HUDID = cmds.headsUpDisplay('HUDTime', section=1, b=6, ba='left' , blockSize='medium', label='Total Time: ', labelFontSize='large', command=getEndTime)

global startT

def getStartTime():
	startT = cmds.timerX()
	return startT

def getEndTime(startT):
	endT = cmds.timerX(st=startT)
	return endT

cmds.hudButton('HUDRecord', s=1, b=5, vis=1, l='Record', bw=60, bsh='roundRectangle', rc=getStartTime, event= 'timeChanged')
cmds.hudButton('HUDStop', s=1, b=5, vis=1, l='Record', bw=60, bsh='roundRectangle',  rc=getEndTime(startT), event= 'timeChanged')


# Now create our button. Only execute on mouse release.
#
cmds.hudButton('HUDHelloButton', s=1, b=5, vis=1, l='Record', bw=60, bsh='roundRectangle',  rc=HUDButtonReleased )

def getStartTime():
    global startT
    startT = cmds.timerX()
    print(startT)
    return startT


def updateTime():
	if cmds.headsUpDisplay('HUDTime', ex=True): # if exists 
		cmds.headsUpDisplay('HUDTime', r=True) # refreshes time
	else:
		cmds.headsUpDisplay('HUDTime', section=1, b=7, ba='left', blockSize='medium', labelFontSize='large', command=getEndTime)

def getEndTime():
    global prevTime
    endT = cmds.timerX(st=startT)
    print(endT)
    return endT


cmds.hudButton('HUDRecord', s=1, b=5, vis=1, l='Record', bw=60, bsh='roundRectangle', rc=getStartTime)
cmds.hudButton('HUDStop', s=1, b=6, vis=1, l='Stop', bw=60, bsh='roundRectangle', rc=getEndTime)


