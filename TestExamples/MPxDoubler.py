import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMaya as OpenMaya
 
class DoublerNode(OpenMayaMPx.MPxNode):
    kPluginNodeId = OpenMaya.MTypeId(0x00000001)
 
    aInput = OpenMaya.MObject()
    aOutput = OpenMaya.MObject()
 
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
 
    def compute(self, plug, data):
        if plug != DoublerNode.aOutput:
            return OpenMaya.MStatus.kUnknownParameter
 
        inputValue = data.inputValue(DoublerNode.aInput).asFloat()
        inputValue *= 2.0
        hOutput = data.outputValue(DoublerNode.aOutput)
        hOutput.setFloat(inputValue)
        data.setClean(plug)
 
        return OpenMaya.MStatus.kSuccess
 
def creator():
    return OpenMayaMPx.asMPxPtr(DoublerNode())
 
def initialize():
    nAttr = OpenMaya.MFnNumericAttribute()
 
    DoublerNode.aOutput = nAttr.create('output', 'out', OpenMaya.MFnNumericData.kFloat)
    nAttr.setWritable(False)
    nAttr.setStorable(False)
    DoublerNode.addAttribute(DoublerNode.aOutput)
 
    DoublerNode.aInput = nAttr.create('input', 'in', OpenMaya.MFnNumericData.kFloat)
    nAttr.setKeyable(True)
    DoublerNode.addAttribute(DoublerNode.aInput)
    DoublerNode.attributeAffects(DoublerNode.aInput, DoublerNode.aOutput)
 
def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Chad Vernon', '1.0', 'Any')
    try:
        plugin.registerNode('doublerNode', DoublerNode.kPluginNodeId, creator, initialize)
    except:
        raise RuntimeError('Failed to register node')
 
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(DoublerNode.kPluginNodeId)
    except:
        raise RuntimeError('Failed to register node')