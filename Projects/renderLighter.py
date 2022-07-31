from builtins import int
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya import OpenMayaUI as omui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import maya.cmds as cmds
import maya.OpenMaya as om
from PySide2 import QtWidgets
import pymel.core as pm
from functools import partial
from shiboken2 import wrapInstance
import logging


customMixinWindow = None

# Delete workspace already present
if not "customMixinWindow" in globals():
    customMixinWindow = None


class camDockableWidget(MayaQWidgetDockableMixin, QWidget):
    """
    This class places a HUD plane for camera attributes
    on the 3D viewport
    """

    lightTypes = {
        "Point Light": pm.pointLight,
        "Spot Light": pm.spotLight,
        "Directional Light": pm.directionalLight,
        "Area Light": partial(pm.shadingNode, 'areaLight', asLight=True),
        "Volume Light": partial(pm.shadingNode, 'volumeLight', asLight=True)
        }

    def __init__(self):
        """
        Constructor: instantiate the camera object and call UI methods
        """
        super().__init__()

        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QGridLayout(self)

        scrollWidget = QtWidgets.QWidget()
        scrollWidget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.scrollLayout = QtWidgets.QVBoxLayout(scrollWidget)
        
        self.tabWidget = QTabWidget()
        layout.addWidget(self.tabWidget, 1, 0, 1, 3)

        initBtn = QtWidgets.QPushButton('Set 3-point light')
        initBtn.clicked.connect(self.createLightRig)
        layout.addWidget(initBtn, 3, 2)

        self.offsetAmount = 10
        self.lightRotation = 30

        defaultOffsetLabel = QtWidgets.QLabel('Vertical Offset')
        defaultOffset = QtWidgets.QLineEdit('10')
        # defaultRotation.valueChanged.connect()
        layout.addWidget(defaultOffsetLabel, 2, 0)
        layout.addWidget(defaultOffset, 2, 1)

        defaultRotationLabel = QtWidgets.QLabel('Rotation Angle')
        lr = str(self.lightRotation)
        defaultRotation = QtWidgets.QLineEdit('30')
        # defaultRotation.textEdited.connect(self.updatelightRotation)
        # defaultRotation.editingFinished.connect(self.editlightRotation())
        # print('value is updated to ' + str(defaultRotation.text()))
        layout.addWidget(defaultRotationLabel, 3, 0)
        layout.addWidget(defaultRotation, 3, 1)

        previewBtn = QtWidgets.QPushButton('Preview')
        previewBtn.clicked.connect(self.aiViewportRender) # TODO: connect
        layout.addWidget(previewBtn, 0, 2)

        self.move(300, 300)
        self.setWindowTitle("Easy Light Rig")
        self.show()

    def updatelightRotation(self):
        print('debug: updating value default lightRotation value')
        # self.lightRotation = 90

    def editlightRotation(self):
        print('debug: editing value default lightRotation value')
        # self.lightRotation = 90

        

    # TODO
    def aiViewportRender(self):
        print('Not yet implemented - this should start viewport render.')

    def createLightRig(self):
        try: 
            selectedNodes = cmds.selectedNodes()
            mainObj = selectedNodes[-1]

            # set object pivots position in world space as the center 
            wsPivots = cmds.xform(mainObj, ws=True, q=True, piv=True)[:-3]  # Get scale pivots
            pvtX, pvtY, pvtZ = wsPivots

            # create key light 
            newLight = cmds.spotLight(rgb=(1, 1, 1), name=mainObj + "KeyLight")
            lightTransform = cmds.listRelatives(newLight, parent=True)
            self.keyLight = lightTransform[0]

            # create fill light
            newLight = cmds.spotLight(rgb=(0.8, 0.8, 0.8), name=mainObj +"FillLight")
            lightTransform = cmds.listRelatives(newLight, parent=True)
            self.fillLight = lightTransform[0]

            # create rim light
            newLight = cmds.directionalLight(rgb=(0.2, 0.2, 0.2), name=mainObj +"RimLight")
            lightTransform = cmds.listRelatives(newLight, parent=True)
            self.rimLight = lightTransform[0]

            # move light to default position 
            cmds.move(pvtX, pvtY, pvtZ + self.offsetAmount, self.keyLight)
            cmds.move(pvtX, pvtY, pvtZ, self.keyLight + ".rotatePivot")
            cmds.rotate(-self.lightRotation, self.lightRotation, 0, self.keyLight)

            cmds.move(pvtX, pvtY, pvtZ + self.offsetAmount, self.fillLight)
            cmds.move(pvtX, pvtY, pvtZ, self.fillLight + ".rotatePivot")
            cmds.rotate(-self.lightRotation, -self.lightRotation, 0, self.fillLight)

            cmds.move(pvtX, pvtY, pvtZ+self.offsetAmount, self.rimLight)
            cmds.move(pvtX, pvtY, pvtZ, self.rimLight + ".rotatePivot")
            cmds.rotate(180 + self.lightRotation, 0, 0, self.rimLight)

            lightNode = cmds.group(empty=True, name= mainObj + "LightRig")

            cmds.parent(self.keyLight, lightNode)
            cmds.parent(self.fillLight, lightNode)
            cmds.parent(self.rimLight, lightNode)

            cmds.select(lightNode, replace=True)

            self.displayGrpTab(mainObj[1:] + "LightRig", mainObj[1:])


        except:
            print('No object is selected.')


    def displayGrpTab(self, grpName, mainObj):
        KeyLightpanelLayout = QGridLayout()
        KeyLightpanel = QWidget()
        KeyLightpanel.setLayout(KeyLightpanelLayout)

        KeyLightCheckBox = QCheckBox(mainObj + "KeyLight")
        self.keylight = pm.PyNode(mainObj+"KeyLight")
        KeyLightCheckBox.setChecked(self.keylight.visibility.get())
        KeyLightCheckBox.toggled.connect(lambda status: self.keylight.getTransform().visibility.set(status)) # visChanged
        KeyLightpanelLayout.addWidget(KeyLightCheckBox, 0, 0)

        KeyLightIntensity = QtWidgets.QSlider(Qt.Horizontal)
        KeyLightRotationl = QtWidgets.QLabel('intensity')
        KeyLightRotationl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        KeyLightpanelLayout.addWidget(KeyLightRotationl, 1, 0)
        KeyLightIntensity.setMinimum(1)
        KeyLightIntensity.setMaximum(1000)
        KeyLightIntensity.setValue(self.keylight.intensity.get())
        KeyLightIntensity.valueChanged.connect(lambda val: self.keylight.intensity.set(val))
        KeyLightpanelLayout.addWidget(KeyLightIntensity, 1, 1, 1, 2)

        KeyLightPos = QtWidgets.QSlider(Qt.Horizontal)
        KeyLightRotationl = QtWidgets.QLabel('position')
        KeyLightRotationl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        KeyLightpanelLayout.addWidget(KeyLightRotationl, 2, 0)
        KeyLightPos.setMinimum(0)
        KeyLightPos.setMaximum(30)
        KeyLightPos.setValue(10)
        # KeyLightRotation.valueChanged.connect(lambda val: self.keylight.lr.set(val))
        KeyLightPos.valueChanged.connect(lambda val: self.keylight.translateZ.set(val))
        KeyLightpanelLayout.addWidget(KeyLightPos, 2, 1, 2, 2)


        KeyLightRotation = QtWidgets.QSlider(Qt.Horizontal)
        KeyLightRotationl = QtWidgets.QLabel('rotation')
        KeyLightRotationl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        KeyLightpanelLayout.addWidget(KeyLightRotationl, 3, 0)

        KeyLightRotation.setMinimum(0)
        KeyLightRotation.setMaximum(90)
        KeyLightRotation.setValue(30)
        # KeyLightRotation.valueChanged.connect(lambda val: self.keylight.lr.set(val))
        KeyLightRotation.valueChanged.connect(lambda val: self.keylight.rotate.set([-val, val, 0]))
        KeyLightpanelLayout.addWidget(KeyLightRotation, 3, 1, 3, 2)
    
    
    # ---------------------------------------------------------------------------

        FillLightpanelLayout = QGridLayout()
        FillLightpanel = QWidget()
        FillLightpanel.setLayout(FillLightpanelLayout)

        FillLightCheckBox = QCheckBox(mainObj + "FillLight")
        self.filllight = pm.PyNode(mainObj+"FillLight")
        FillLightCheckBox.setChecked(self.filllight.visibility.get())
        FillLightCheckBox.toggled.connect(lambda status: self.filllight.getTransform().visibility.set(status)) # visChanged
        FillLightpanelLayout.addWidget(FillLightCheckBox, 0, 0)


        FillLightIntensity = QtWidgets.QSlider(Qt.Horizontal)
        FillLightRotationl = QtWidgets.QLabel('intensity')
        FillLightRotationl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        FillLightpanelLayout.addWidget(FillLightRotationl, 1, 0)
        FillLightIntensity.setMinimum(1)
        FillLightIntensity.setMaximum(1000)
        FillLightIntensity.setValue(self.filllight.intensity.get())
        FillLightIntensity.valueChanged.connect(lambda val: self.filllight.intensity.set(val))
        FillLightpanelLayout.addWidget(FillLightIntensity, 1, 1, 1, 2)


        FillLightPos = QtWidgets.QSlider(Qt.Horizontal)
        FillLightRotationl = QtWidgets.QLabel('position')
        FillLightRotationl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        FillLightpanelLayout.addWidget(FillLightRotationl, 2, 0)
        FillLightPos.setMinimum(0)
        FillLightPos.setMaximum(30)
        FillLightPos.setValue(10)
        FillLightPos.valueChanged.connect(lambda val: self.filllight.translateZ.set(val))
        FillLightpanelLayout.addWidget(FillLightPos, 2, 1, 2, 2)

        FillLightRotation = QtWidgets.QSlider(Qt.Horizontal)
        FillLightRotationl = QtWidgets.QLabel('rotation')
        FillLightRotationl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        FillLightpanelLayout.addWidget(FillLightRotationl, 3, 0)

        FillLightRotation.setMinimum(0)
        FillLightRotation.setMaximum(90)
        FillLightRotation.setValue(30)
        FillLightRotation.valueChanged.connect(lambda val: self.filllight.rotate.set([-val, val, 0]))
        FillLightpanelLayout.addWidget(FillLightRotation, 3, 1, 3, 2)


     # ---------------------------------------------------------------------------



        RimLightpanelLayout = QGridLayout()
        RimLightpanel = QWidget()
        RimLightpanel.setLayout(RimLightpanelLayout)

        RimLightCheckBox = QCheckBox(mainObj + "RimLight")
        self.rimlight = pm.PyNode(mainObj+"RimLight")
        RimLightCheckBox.setChecked(self.rimlight.visibility.get())
        RimLightCheckBox.toggled.connect(lambda status: self.rimlight.getTransform().visibility.set(status)) # visChanged
        RimLightpanelLayout.addWidget(RimLightCheckBox, 0, 0)


        RimLightIntensity = QtWidgets.QSlider(Qt.Horizontal)
        RimLightRotationl = QtWidgets.QLabel('intensity')
        RimLightRotationl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        RimLightpanelLayout.addWidget(RimLightRotationl, 1, 0)
        RimLightIntensity.setMinimum(1)
        RimLightIntensity.setMaximum(1000)
        RimLightIntensity.setValue(self.rimlight.intensity.get())
        RimLightIntensity.valueChanged.connect(lambda val: self.rimlight.intensity.set(val))
        RimLightpanelLayout.addWidget(RimLightIntensity, 1, 1, 1, 2)


        RimLightPos = QtWidgets.QSlider(Qt.Horizontal)
        RimLightRotationl = QtWidgets.QLabel('position')
        RimLightRotationl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        RimLightpanelLayout.addWidget(RimLightRotationl, 2, 0)
        RimLightPos.setMinimum(0)
        RimLightPos.setMaximum(30)
        RimLightPos.setValue(10)
        RimLightPos.valueChanged.connect(lambda val: self.rimlight.translateZ.set(val))
        RimLightpanelLayout.addWidget(RimLightPos, 2, 1, 2, 2)

        RimLightRotation = QtWidgets.QSlider(Qt.Horizontal)
        RimLightRotationl = QtWidgets.QLabel('rotation')
        RimLightRotationl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        RimLightpanelLayout.addWidget(RimLightRotationl, 3, 0)

        RimLightRotation.setMinimum(0)
        RimLightRotation.setMaximum(90)
        RimLightRotation.setValue(30)
        RimLightRotation.valueChanged.connect(lambda val: self.rimlight.rotate.set([-val, val, 0]))
        RimLightpanelLayout.addWidget(RimLightRotation, 3, 1, 3, 2)


     # ---------------------------------------------------------------------------

        # Add three light panels to the tab 
        tabPage = QWidget()
        tabLayout = QGridLayout()
        tabPage.setLayout(tabLayout)
        tabLayout.addWidget(KeyLightpanel, 0, 0)
        tabLayout.addWidget(FillLightpanel, 1, 0)
        tabLayout.addWidget(RimLightpanel, 2, 0)
        
        # Rename the tab to group name, and add to interface display
        self.tabWidget.addTab(tabPage, grpName)


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
        customMixinWindow.setObjectName("customMayaMixinWindow")

    if restore == True:
        # Add custom mixin widget to the workspace control
        mixinPtr = omui.MQtUtil.findControl(customMixinWindow.objectName())
        omui.MQtUtil.addWidgetToMayaLayout(int(mixinPtr), int(restoredControl))
    else:
        # Create a workspace control for the mixin widget by passing all the 
        # needed parameters. See workspaceControl command documentation for 
        # all available flags.
        customMixinWindow.show(
            dockable=True,
            height=600,
            width=480,
            uiScript="camDockableWidgetUIScript(restore=True)",
        )

    return customMixinWindow


def main():
    ui = camDockableWidgetUIScript()
    return ui


if __name__ == "__main__":
    main()
