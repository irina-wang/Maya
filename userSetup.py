# userSetup.py

import maya.cmds as cmds

cmds.sphere()

"""
Read from standard input 

"""
import sys

inp = sys.stdin.readline()


import maya.cmds as cmds

inp = cmds.promptDialog(message="hello")
