import maya.standalone

maya.standalone.initialize()

try:
    import maya.standalone

    maya.standalone.initialize()
except:
    pass


try:
    maya.standalone.uninitialize()
except:
    pass
