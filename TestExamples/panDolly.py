import maya.cmds as cmds

# Save the current position of the persp camera.
homeName = cmds.cameraView(camera='persp')

# Add this view to the persp bookmark menu.
cmds.cameraView( homeName, e=True, camera='persp', ab=True )

# Change the persp camera position.
cmds.dolly( 'persp', distance=-30 )

# Create another bookmark for the zoomed position.
cmds.cameraView( camera='persp', name='zoom', ab=True )

# Restore original camera position.
cmds.cameraView( homeName, e=True, camera='persp', sc=True )

# Save the current 2D pan/zoom attributes of the persp camera
panZoomBookmark = cmds.cameraView( camera='persp', ab=True, typ=1 )

# Enable 2D pan/zoom
cmds.setAttr( 'perspShape.panZoomEnabled', True )

# Pan right
cmds.panZoom( 'persp', r=0.6 )

# Restore original film position
cmds.cameraView( panZoomBookmark, e=True, camera='persp', sc=True )
