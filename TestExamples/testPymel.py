import pymel.core as pm

from pymel.core import *


help(pm.nt)

import maya.cmds as cmds


import pymel.core.nt.Transform 


def findCenterCoordinate(self,transform, index):
    face = pm.MeshFace("%s.f[%s]" % (transform, index))
    pt = face.__apimfn__().center(OpenMaya.MSpace.kWorld)
    centerPoint = pm.datatypes.Point(pt)
    return centerPoint
    
p = polySphere( name='theMoon', sa=7, sh=7 )[0]

print(pm.nt.getPosition(p))




findCenterCoordinate(pCube1[0],1)


