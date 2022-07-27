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
    newLight = cmds.spotLight(rgb=(1, 1, 1), name="KeyLight")
    lightTransform = cmds.listRelatives(newLight, parent=True)
    keyLight = lightTransform[0]

    # create fill light
    newLight = cmds.spotLight(rgb=(0.8, 0.8, 0.8), name="FillLight")
    lightTransform = cmds.listRelatives(newLight, parent=True)
    fillLight = lightTransform[0]

    # create rim light
    newLight = cmds.directionalLight(rgb=(0.2, 0.2, 0.2), name="RimLight")
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

    lightNode = cmds.group(empty=True, name="LightRig")

    cmds.parent(keyLight, lightNode)
    cmds.parent(fillLight, lightNode)
    cmds.parent(rimLight, lightNode)

    cmds.select(lightNode, replace=True)


def centerPivot(mainObj):
    cmds.xform(mainObj, cpc=True)


selectedNodes = cmds.selectedNodes()
selectedObj = selectedNodes[-1]
createLightRig(selectedObj)




sel = cmds.ls(sl=True)[0]

cmds.xform(sel, cpc=True)  # Center its pivot. Comment this out if you don't want to force it to center and use the pivot as-is.
pivots = cmds.xform(sel, ws=True, q=True, piv=True)[:-3]  # Get its pivot values.

print(pivots)


# 
sel = cmds.ls(sl=True)[0]  # Get selection.

# cmds.xform(sel, cpc=True)  # Center its pivot. Comment this out if you don't want to force it to center and use the pivot as-is.
# pivots = cmds.xform(sel, q=True, piv=True)[:3]  # Get its pivot values.

# temp_nul = cmds.createNode("transform")  # Create a temporary transform.
# cmds.matchTransform(temp_nul, sel)  # Align the transform to our object.

# try:
#     cmds.xform(sel, piv=[0, 0, 0])  # Zero-out object's pivot values.
#     cmds.move(-pivots[0], -pivots[1], -pivots[2], "{}.vtx[*]".format(sel), os=True, r=True)  # Negate and move object via its old pivot values.
#     cmds.matchTransform(sel, temp_nul)  # Align the object back to the temporary transform, to maintain its old position.
# finally:
#     cmds.delete(temp_nul)  # Delete temporary transform.
#     cmds.select(sel)  # Restore old selection.



