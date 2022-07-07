################################################################################
# Author: Irina Mengqi Wang, 07/2022 
# Project: Camera_HUD (In-Progress)
#
# --------
# Outline: 
#       1. heads-up display (HUD): basic UI programming in Maya 
#   --> 2. Autofocus (Reticle)                                      IN-PROGRESS
#       3. Customizable camera shakes                               IN-PROGRESS
#
################################################################################

from builtins import int
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya import OpenMayaUI as omui
from PySide2.QtCore import * 
from PySide2.QtGui import * 
from PySide2.QtWidgets import *
import maya.cmds as cmds


customMixinWindow = None

# Delete workspace already present
if not 'customMixinWindow' in globals():
    customMixinWindow = None

class camDockableWidget(MayaQWidgetDockableMixin, QWidget):
    """ 
        This class places a HUD plane for camera attributes 
        on the 3D viewport
    """
    def __init__(self):
        """
        Constructor: instantiate the camera object and call UI methods
        """
        super().__init__()
        self.cameraName = cmds.camera()
        self.initUI()


    def initUI(self):
        """
        Initialize the widget UI
        """        
        # Tab 1: HeadUpDisplay
        # create Checkbox for each attribute to be displayed
        
        self.NameCheckBox = QCheckBox('Camera Name')
        self.NameCheckBox.stateChanged.connect(self.CamNameOnOff)

        self.PosCheckBox = QCheckBox('Position')
        self.PosCheckBox.stateChanged.connect(self.PosOnOff)

        self.FocalCheckBox = QCheckBox('Focal Length')
        self.FocalCheckBox.stateChanged.connect(self.FocalOnOff)

        self.ZoomCheckBox = QCheckBox('Zoom')
        self.ZoomCheckBox.stateChanged.connect(self.ZoomOnOff)
        
        # add checkbox to layout 
        tabPage = QWidget()
        tabLayout = QVBoxLayout()
        tabPage.setLayout(tabLayout)
        tabLayout.addWidget(self.NameCheckBox)
        tabLayout.addWidget(self.PosCheckBox)
        tabLayout.addWidget(self.FocalCheckBox)
        tabLayout.addWidget(self.ZoomCheckBox)

        # !!!!!!!!!!!!!!!!!!!!!! TODO !!!!!!!!!!!!!!!!!!!!!!!! 
        # Tab2: Camera Control
        label2 = QLabel("Widget in Tab 2 for Camera Control.")

        # Tab3: Camera Shake
        label3 = QLabel("Widget in Tab 3 for Camera Shake.")
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Create tab widgets
        # append tabs to the tabWidget 
        tabWidget = QTabWidget()
        tabWidget.addTab(tabPage, "Display")
        tabWidget.addTab(label2, "Camera Control")
        tabWidget.addTab(label3, "Camera Shake")

        # Grid layout for tabs
        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(tabWidget, 0, 0)

        self.move(300, 300)
        self.setWindowTitle('Camera Heads-Up-Display Control')
        self.show()

    # ========================================================
    #  
    #   Methods to get attribute value. 
    #
    # ========================================================

    def getFocal(self):
        """
        Get the focal length of the selected camera
        """
        cameraShape = self.cameraName[1] 
        camfocalLength = cmds.camera(cameraShape, q=True, fl=True)
        return camfocalLength

    def getZoom(self):
        """
        Get the Zoom length for the selected camera
        """
        cameraShape = self.cameraName[1]
        camZoom =  cmds.camera(cameraShape, q=True, e=True, zom=True)
        return camZoom

    def getCamName(self):
        """
        Get Camera name, change upon selection node change
        TODO: check if the object is a camera
        """
        try:
            selectedNodes = cmds.selectedNodes()
            mainObj = selectedNodes[-1]
            return mainObj[1:] # format the name 
        except:
            print('Error: No object selected. ')
            return ''
	
    def getObjectPosition(*args):
        """
        Get the object position of the selected item
        TODO: check if the object is a camera
        """
        try:
            selectedNodes = cmds.selectedNodes() 
            mainObj = selectedNodes[-1] # get the select node
            positionList = cmds.getAttr('%s.translate' % mainObj) 
            return positionList[0]
        except:
            return (0.0,0.0,0.0)

    # ========================================================
    #  
    #   Methods to control section display On/Off.
    #
    # ========================================================

    def CamNameOnOff(self):
        if self.NameCheckBox.isChecked():
            cmds.headsUpDisplay( 'HUDName', section=1, b=0, ba='left' , blockSize='medium', label='Cam', labelFontSize='large', command=self.getCamName, event='SelectionChanged', nodeChanges='attributeChange' )
        else:
            cmds.headsUpDisplay( 'HUDName', rem=True )

    def PosOnOff(self):
        if self.PosCheckBox.isChecked():
            cmds.headsUpDisplay( 'HUDObjectPosition', section=1, block=1, blockSize='medium', label='Position', labelFontSize='large', command=self.getObjectPosition, event='SelectionChanged', nodeChanges='attributeChange')        
        else:
            cmds.headsUpDisplay( 'HUDObjectPosition', rem=True )

    def ZoomOnOff(self):
        if self.ZoomCheckBox.isChecked():
            cmds.headsUpDisplay( 'HUDZoom', section=3, block=0, blockSize='medium', label='Zoom', labelFontSize='large', command=self.getZoom, atr=True)
        else:
            cmds.headsUpDisplay( 'HUDZoom', rem=True )

    def FocalOnOff(self):
        if self.FocalCheckBox.isChecked():
            cmds.headsUpDisplay( 'HUDFocal', section=2, block=0, blockSize='medium', label='Focal', labelFontSize='large', command=self.getFocal, atr=True)
        else:
            cmds.headsUpDisplay( 'HUDFocal', rem=True )


def camDockableWidgetUIScript(restore=False):
    """ 
        When the control is restoring, the workspace control has already been 
        created and all that needs to be done is restoring its UI.
    """
    global customMixinWindow
    if restore == True:
        # Grab the created workspace control with the following.
        restoredControl = omui.MQtUtil.getCurrentParent()
  
    if customMixinWindow is None:
        # Create a custom mixin widget for the first time
        customMixinWindow = camDockableWidget()     
        customMixinWindow.setObjectName('customMayaMixinWindow')
        
    if restore == True:
        # Add custom mixin widget to the workspace control
        mixinPtr = omui.MQtUtil.findControl(customMixinWindow.objectName())
        omui.MQtUtil.addWidgetToMayaLayout(int(mixinPtr), int(restoredControl))
    else:
        # Create a workspace control for the mixin widget by passing all the needed parameters. See workspaceControl command documentation for all available flags.
        customMixinWindow.show(dockable=True, height=600, width=480, uiScript='camDockableWidgetUIScript(restore=True)')
        
    return customMixinWindow
      
def main():
    ui = camDockableWidgetUIScript()
    return ui

if __name__ == '__main__':
    main()
