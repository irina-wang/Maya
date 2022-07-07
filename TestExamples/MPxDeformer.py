import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
import maya.cmds as cmds
 
class BlendNode(OpenMayaMPx.MPxDeformerNode):
    kPluginNodeId = OpenMaya.MTypeId(0x00000002)
     
    aBlendMesh = OpenMaya.MObject()
    aBlendWeight = OpenMaya.MObject()
     
    def __init__(self):
        OpenMayaMPx.MPxDeformerNode.__init__(self)
 
    def deform(self, data, itGeo, localToWorldMatrix, mIndex):
        envelope = OpenMayaMPx.cvar.MPxDeformerNode_envelope
        env = data.inputValue(envelope).asFloat()
        blendWeight = data.inputValue(BlendNode.aBlendWeight).asFloat()
        blendWeight *= env
 
        oBlendMesh = data.inputValue(BlendNode.aBlendMesh).asMesh()
        if oBlendMesh.isNull():
            return OpenMaya.MStatus.kSuccess
 
        fnBlendMesh = OpenMaya.MFnMesh(oBlendMesh)
        blendPoints = OpenMaya.MPointArray()
        fnBlendMesh.getPoints(blendPoints)
 
        while not itGeo.isDone():
            pt = itGeo.position()
            w = self.weightValue(data, mIndex, itGeo.index())
            pt = pt + (blendPoints[itGeo.index()] - pt) * blendWeight * w
            itGeo.setPosition(pt)
            itGeo.next()
 
        return OpenMaya.MStatus.kSuccess
 
def creator():
    return OpenMayaMPx.asMPxPtr(BlendNode())
 
def initialize():
    tAttr = OpenMaya.MFnTypedAttribute()
    nAttr = OpenMaya.MFnNumericAttribute()
     
    BlendNode.aBlendMesh = tAttr.create('blendMesh', 'bm', OpenMaya.MFnData.kMesh)
    BlendNode.addAttribute( BlendNode.aBlendMesh )
     
    outputGeom = OpenMayaMPx.cvar.MPxDeformerNode_outputGeom
    BlendNode.attributeAffects(BlendNode.aBlendMesh, outputGeom)
 
    BlendNode.aBlendWeight = nAttr.create('blendWeight', 'bw', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    BlendNode.addAttribute(BlendNode.aBlendWeight)
    BlendNode.attributeAffects(BlendNode.aBlendWeight, outputGeom)
 
    # Make deformer weights paintable
    cmds.makePaintable('blendNode', 'weights', attrType='multiFloat', shapeMode='deformer')
 
def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Chad Vernon', '1.0', 'Any')
    try:
        plugin.registerNode('blendNode', BlendNode.kPluginNodeId, creator, initialize, OpenMayaMPx.MPxNode.kDeformerNode)
    except:
        raise RuntimeError('Failed to register node')
 
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(BlendNode.kPluginNodeId)
    except:
        raise RuntimeError('Failed to deregister node')