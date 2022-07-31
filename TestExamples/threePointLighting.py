import maya.cmds as cmds



# control={ offsetAmount = 10, 
#         lightRotation = 30, 
#         vis = 'True',
#         i = 1.0,
#         r = 0.8,
#         g = 0.8,
#         b = 0.8
# }
def createLightRig(mainObj):

    # get object position & object space pivot 
    # objPositionList = cmds.getAttr('%s.translate' % mainObj)[0] # maybe to set plans 
    # scalePivotList = cmds.getAttr('%s.scalePivot' % mainObj)[0] #
    # rotatePivotList = cmds.getAttr('%s.rotatePivot' % mainObj)[0] #

    offsetAmount = 10
    lightRotation = 30

    # set object pivots position in world space as the center 
    wsPivots = cmds.xform(mainObj, ws=True, q=True, piv=True)[:-3]  # Get scale pivots
    pvtX, pvtY, pvtZ = wsPivots

    
    # create key light 
    newLight = cmds.spotLight(rgb=(1, 1, 1), name=mainObj + "KeyLight")
    lightTransform = cmds.listRelatives(newLight, parent=True)
    keyLight = lightTransform[0]

    # create fill light
    newLight = cmds.spotLight(rgb=(0.8, 0.8, 0.8), name=mainObj +"FillLight")
    lightTransform = cmds.listRelatives(newLight, parent=True)
    fillLight = lightTransform[0]

    # create rim light
    newLight = cmds.directionalLight(rgb=(0.2, 0.2, 0.2), name=mainObj +"RimLight")
    lightTransform = cmds.listRelatives(newLight, parent=True)
    rimLight = lightTransform[0]

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # TEST - create area light
    # newLight = cmds.shadingNode('areaLight', asLight=True, name=mainObj +"areaLight")
    # lightTransform = cmds.listRelatives(newLight, parent=True)
    # areaLight = lightTransform[0] 
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
    # move light to default position 
    cmds.move(pvtX, pvtY, pvtZ + offsetAmount, keyLight)
    cmds.move(pvtX, pvtY, pvtZ, keyLight + ".rotatePivot")
    cmds.rotate(-lightRotation, lightRotation, 0, keyLight)

    cmds.move(pvtX, pvtY, pvtZ + offsetAmount, fillLight)
    cmds.move(pvtX, pvtY, pvtZ, fillLight + ".rotatePivot")
    cmds.rotate(-lightRotation, -lightRotation, 0, fillLight)

    cmds.move(pvtX, pvtY, pvtZ+offsetAmount, rimLight)
    cmds.move(pvtX, pvtY, pvtZ, rimLight + ".rotatePivot")
    cmds.rotate(180 + lightRotation, 0, 0, rimLight)

# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # cmds.move(pvtX, pvtY, pvtZ + offsetAmount, areaLight)
    # cmds.move(pvtX, pvtY, pvtZ, areaLight + ".rotatePivot")
    # cmds.rotate(-lightRotation, -lightRotation, 0, areaLight)
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    lightNode = cmds.group(empty=True, name= mainObj + "LightRig")

    cmds.parent(keyLight, lightNode)
    cmds.parent(fillLight, lightNode)
    cmds.parent(rimLight, lightNode)
    # cmds.parent(areaLight, lightNode)

    cmds.select(lightNode, replace=True)


def centerPivot(obj):
    cmds.xform(obj, cpc=True)


def LightUpdate(LightType, obj, vis, i, r,g,b):
    '''
    Update intensity, rgb, value while the update button is clicked

    Examples: 
        LightUpdate(obj +'KeyLight', , 1.0, vis, r,g,b) 
        LightUpdate(obj + 'FillLight', obj, 1.0, vis, r,g,b) 
        LightUpdate(obj + 'RimLight', obj, 1.0, vis, r,g,b) 

    other flags:
        https://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/CommandsPython/pointLight.html#hExamples
    '''
    objName = obj + LightType

    # Highlight the object
    cmds.select(clear=True)
    cmds.select(objName)

    # Update intensity
    cmds.setAttr(objName + ".intensity", i)
    # print('Debug Info: Object Intensity is set to ' + str(cmds.getAttr(objName + ".intensity")))

    # Update visibility 
    cmds.setAttr(objName + '.visibility', vis)
    # flip visibility 
    # cmds.setAttr(objName + '.visibility', not cmds.getAttr(objName +'.visibility'))
    
    # Update rgb (assume it's spotlight)
    cmds.spotLight(objName, e=True, rgb=(r, g, b))
    # cmds.spotLight('pCube1KeyLight', q=True, rgb=True)


'''
    How to use
'''
selectedNodes = cmds.selectedNodes()
try: 
   selectedObj = selectedNodes[-1]
   createLightRig(selectedObj)
except: 
   print('No object is selected')