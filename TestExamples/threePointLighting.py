import maya.cmds as cmds

def createLightRig(mainObj):

    # get object position
    objPositionList = cmds.getAttr('%s.translate' % mainObj)[0]
    scalePivotList = cmds.getAttr('%s.scalePivot' % mainObj)[0]
    rotatePivotList = cmds.getAttr('%s.rotatePivot' % mainObj)[0]
    # pvtX, pvtY, pvtZ = scalePivotList

    # get world pivots
    pivots = cmds.xform(mainObj, ws=True, q=True, piv=True)[:-3]  # Get its pivot values.
    pvtX, pvtY, pvtZ = pivots

    offsetAmount = 10
    lightRotation = 30

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

    cmds.move(pvtX, pvtY, pvtZ + offsetAmount, keyLight)
    cmds.move(pvtX, pvtY, pvtZ, keyLight + ".rotatePivot")
    cmds.rotate(-lightRotation, lightRotation, 0, keyLight)

    cmds.move(pvtX, pvtY, pvtZ + offsetAmount, fillLight)
    cmds.move(pvtX, pvtY, pvtZ, fillLight + ".rotatePivot")
    cmds.rotate(-lightRotation, -lightRotation, 0, fillLight)

    cmds.move(pvtX, pvtY, pvtZ+offsetAmount, rimLight)
    cmds.move(pvtX, pvtY, pvtZ, rimLight + ".rotatePivot")
    cmds.rotate(180 + lightRotation, 0, 0, rimLight)

    lightNode = cmds.group(empty=True, name= mainObj + "LightRig")

    cmds.parent(keyLight, lightNode)
    cmds.parent(fillLight, lightNode)
    cmds.parent(rimLight, lightNode)

    cmds.select(lightNode, replace=True)

    return keyLight


def centerPivot(mainObj):
    cmds.xform(mainObj, cpc=True)

# lightShape - name of the light
# intensity - float
def setColor(lightShape, intensity):
    cmds.setAttr(lightShape + ".intensity", intensity)


selectedNodes = cmds.selectedNodes()
selectedObj = selectedNodes[-1]
lightNode = createLightRig(selectedObj)
print(lightNode)

# cmds.setAttr(keyLight + ".intensity", 0.5)
# cmds.setAttr(keyLightShape + ".intensity", 0.5)





