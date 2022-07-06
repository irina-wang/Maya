# Author: Irina Mengqi Wang, 07/2022 
# Project: Camera_HUD (In-Progress)
# --------
# Outline: 
#       1. heads-up display (HUD) - basic UI programming in Maya 
#   --> 2. Autofocus tools (Reticle)
#       3. Customizable camera shakes


from builtins import int
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya import OpenMayaUI as omui
from PySide2.QtCore import * 
from PySide2.QtGui import * 
from PySide2.QtWidgets import *
import maya.cmds as cmds


customMixinWindow = None

# check 
if not 'customMixinWindow' in globals():
    customMixinWindow = None
    
class DockableWidget(MayaQWidgetDockableMixin, QWidget):

    def __init__(self):
        '''
        Constructor: instantiate the camera object and call UI methods

        '''
        super().__init__()
        self.cameraName = cmds.camera()
        self.initUI()


    def initUI(self):
        '''
        Initialize the widget UI

        '''
        # create a checkbox control for HeadUpDisplay 
        self.checkBox = QCheckBox('HUD', self)
        self.checkBox.stateChanged.connect(self.OnOff)

        # arrange the box in the layout 
        layout = QHBoxLayout()
        layout.addWidget(self.checkBox)
        layout.addStretch(1)
        self.setLayout(layout)

        self.move(300, 300)
        self.setWindowTitle('Camera Heads Up Display Control')
        self.show()


    def getFocal(self):
        '''
        Get the focal length of the selected camera

        '''
        cameraShape = self.cameraName[1]
        camfocalLength = cmds.camera(cameraShape, q=True, fl=True)
        return camfocalLength

    def getZoom(self):
        '''
        Get the Zoom length for the selected camera

        '''
        cameraShape = self.cameraName[1]
        camZoom =  cmds.camera(cameraShape, q=True, e=True, zom=True)
        return camZoom


    def objectPosition(*args):
        '''
        Get the object position of the selected item

        '''

        try:
            selectedNodes = cmds.selectedNodes() 
            mainObj = selectedNodes[-1] # get the select node
            positionList = cmds.getAttr('%s.translate' % mainObj) 
            return positionList[0]
        except:
            return (0.0,0.0,0.0)


    def OnOff(self):
        '''
        Respond to the toggling of a checkbox, display the HUD when box is 
        checked and vice versa. 

        '''
        if self.checkBox.isChecked():
            # print("CHECKED!")
            cmds.headsUpDisplay( 'HUDObjectPosition', section=1, block=0, blockSize='medium', label='Position', labelFontSize='large', command=self.objectPosition, event='SelectionChanged', nodeChanges='attributeChange' )
            cmds.headsUpDisplay( 'HUDFocal', section=2, block=0, blockSize='medium', label='Focal', labelFontSize='large', command=self.getFocal, event='SelectionChanged', nodeChanges='attributeChange' )
            cmds.headsUpDisplay( 'HUDZoom', section=3, block=0, blockSize='medium', label='Zoom', labelFontSize='medium', command=self.getZoom, event='SelectionChanged', nodeChanges='attributeChange' )
        else:
            # print("UNCHECKED!")
            cmds.headsUpDisplay( 'HUDObjectPosition', rem=True )
            cmds.headsUpDisplay( 'HUDFocal', rem=True )
            cmds.headsUpDisplay( 'HUDZoom', rem=True )


def DockableWidgetUIScript(restore=False):
    ''' 
        When the control is restoring, the workspace control has already been 
        created and all that needs to be done is restoring its UI.
    '''
    global customMixinWindow
    if restore == True:
        # Grab the created workspace control with the following.
        restoredControl = omui.MQtUtil.getCurrentParent()
  
    if customMixinWindow is None:
        # Create a custom mixin widget for the first time
        customMixinWindow = DockableWidget()     
        customMixinWindow.setObjectName('customMayaMixinWindow')
        
    if restore == True:
        # Add custom mixin widget to the workspace control
        mixinPtr = omui.MQtUtil.findControl(customMixinWindow.objectName())
        omui.MQtUtil.addWidgetToMayaLayout(int(mixinPtr), int(restoredControl))
    else:
        # Create a workspace control for the mixin widget by passing all the needed parameters. See workspaceControl command documentation for all available flags.
        customMixinWindow.show(dockable=True, height=600, width=480, uiScript='DockableWidgetUIScript(restore=True)')
        
    return customMixinWindow
      
def main():
    ui = DockableWidgetUIScript()
    return ui

if __name__ == '__main__':
    main()
