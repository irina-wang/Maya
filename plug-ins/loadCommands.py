import maya.cmds as cmds


def load_plugin(name):
    cmds.loadPlugin(name)

def unload_plugin(name):
    pass

def is_plugin_loaded(name):
    pass


if __name__ == '__main__':
    plugin_name = 'myFirstPlugin'