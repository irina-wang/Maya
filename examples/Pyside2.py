  from Pyside2.QtCore import * 
  
  hello = QLabel("Hello, World", parent=mayaMainWindow) 
  hello.setObjectName('MyLabel') 
  hello.setWindowFlags(Qt.Window) # Make this widget a parented standalone window
  hello.show() 
  hello = None # widget is parented, so it will not be destroyed. 