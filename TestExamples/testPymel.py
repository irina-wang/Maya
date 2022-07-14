import pymel.core as pm
from pymel.core import *


def findCenterCoordinate(self,transform, index):
    face = pm.MeshFace("%s.f[%s]" % (transform, index))
    pt = face.__apimfn__().center(OpenMaya.MSpace.kWorld)
    centerPoint = pm.datatypes.Point(pt)
    return centerPoint
    
p = polySphere( name='theMoon', sa=7, sh=7 )[0]

print(pm.nt.getPoints(p))
print(p.vtx[9])


pm.Mesh.getClosestPoint(p.vtx[9], space='preTransform', accelParams=None)


p.getClosestPoint(dt.Point(0.0,0.0,0.0))



# print the position of the vertex
print(p.vtx[9].getPosition())

