''' 
Learning document
https://help.autodesk.com/view/MAYAUL/2017/ENU/?guid=__files_GUID_FE0662C0_4F1A_46BE_9828_76656C2BD2E2_html

Mengqi Irina Wang 

'''



''' Maya 1.0 '''
import maya.api.OpenMaya       as OpenMaya        # Common classes
import maya.api.OpenMayaAnim   as OpenMayaAnim    # Animation classes
import maya.api.OpenMayaRender as OpenMayaRender  # Rendering classes
import maya.api.OpenMayaUI     as OpenMayaUI      # User interface classes

# Maya 1.0
import maya.OpenMaya       as OpenMaya        # Common classes
import maya.OpenMayaMPx    as OpenMayaMPx     # Classes from which to inherit
import maya.OpenMayaAnim   as OpenMayaAnim    # Animation classes
import maya.OpenMayaFX     as OpenMayaFX      # Effect classes (hair, particles, fluids)
import maya.OpenMayaRender as OpenMayaRender  # Rendering classes
import maya.OpenMayaUI     as OpenMayaUI      # User interface classes
import maya.OpenMayaCloth  as OpenMayaCloth   # Cloth classes


'''
Entry and Exit Points: 
Maya plug-ins require two specific functions. If these two functions do not
exist in the file, the plug-in will fail to load.

Code is derived from the MPxCommand class. 

'''
def initializePlugin( mobject ):
    ''' Initialize the plug-in when Maya loads it. '''

def uninitializePlugin( mobject ):
    ''' Uninitialize the plug-in when Maya un-loads it. '''



# kPluginCmdName

class MyCommandClass( OpenMayaMPx.MPxCommand ):
    
    def __init__(self):
        ''' Constructor. '''
    
    def doIt(self, args):
        ''' Command execution. '''        
        pass

    '''
    cmdCreator
        a maya_useNewAPI() function must be defined to indicate what type objects 
    are being passed.
    '''