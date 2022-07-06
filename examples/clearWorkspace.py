# Save as BBTest.py in your Maya script path
import pymel.core as pm

WorkspaceName = 'WorkspaceWinBoo'

class BBTest(object):
    def StartUI(self):
        if pm.workspaceControl( WorkspaceName, query=True, exists=True) is False:
            pm.workspaceControl( WorkspaceName, uiScript = 'from BBTest import curUI\ncurUI.buildUI()', closeCommand='from BBTest import curUI\ncurUI.CloseUI()')
        else:
            pm.workspaceControl( WorkspaceName, edit=True, restore=True)
        
    def CloseUI(self):
        if pm.workspaceControl( WorkspaceName, query=True, exists=True):
            pm.workspaceControl( WorkspaceName, edit=True, close=True )
    
    
    def buildUI(self):
        WinLayout = pm.columnLayout( adjustableColumn=True )
        pm.button( label='Do Nothing' )
        pm.button( label='Close', command=pm.Callback(self.CloseUI) )

curUI = BBTest()