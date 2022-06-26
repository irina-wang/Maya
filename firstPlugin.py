'''

Got inspiration from 
https://www.artstation.com/blogs/mvanneutigem/pL67/writing-a-basic-maya-plugin-in-python





'''

from tkinter.filedialog import Open
from unicodedata import numeric
from maya import cmds
from maya.api import OpenMaya

maya_useNewAPI = True

class demoNode(OpenMaya.MPxNode):
    type_id = OpenMaya.MTypeId(0x00000000)
    type_name = 'demoNode'


    # attributes 
    input_one = None
    input_two = None
    output = None

    def _init_(self):
        OpenMaya.MPxNode._init_(self)

    @classmethod
    def initialize(cls):
        ''' Create the plugin attributes and dependecies here.'''

        # type of attribute to create 
        numeric_attr = OpenMaya.MFnNumerricAttribute()

        # input_one 
        cls.input_one = numeric_attr.create(
            'inputOne', # longname
            'io', # shortname
            OpenMaya.MFnNumericAttribute.kFloat # attribute type
        )

        numeric_attr.readable = False # no Input 
        numeric_attr.writable = True
        numeric_attr.keyable = True

        cls.addAttribute(cls.input_one)

        # input_two 
        cls.input_two = numeric_attr.create(
            'inputTwo', # longname
            'it', # shortname
            OpenMaya.MFnNumericAttribute.kFloat # attribute type
        )

        numeric_attr.readable = False # no Input 
        numeric_attr.writable = True
        numeric_attr.keyable = True

        cls.addAttribute(cls.input_one)

        # create last attribute to the class
        cls.output = numeric_attr.create(
            'output', # longname
            'o', # shortname
            OpenMaya.MFnNumericAttribute.kFloat # attribute type
        )

        numeric_attr.readable = True # no Input 
        numeric_attr.writable = False

        cls.attributeAffects(cls.input_one)

        # add dependencies 
        cls.addAttribute(cls.input_one, cls.output)
        cls.addAttribute(cls.input_two, cls.output)

    @classmethod
    def creator(cls):
        ''' Create a class instance here.'''
        return cls()

    def computer(self, plug, data_block):
        ''' Compute any data here, inherits from mpxnode.compute
        
        Args: 
            plug (MPlug):
                plug representing the attribute that needs to be recomputed. 
            data_block (MDataBlock):
                data block containing storage for the node's attributes.
        '''

        if plug == self.output:
            # get data from input attrs
            input_one_value = data_block.inputValue(self.input_one).asFloat()
            input_two_value = data_block.inputValue(self.input_two).asFloat()

            average = (input_one_value + input_two_value) / 2.0

            # get output handle, set its value, and set it as clean
            output_handle = data_block.outputValue(self.output)
            output_handle.setFloat(average)
            output_handle.setClean()



    def initializePlugin(plugin):
        ''' Called when the plugin is loaded in Maya
        
        Args: 
            plug (MObject):
               the plugin to initialize.
        '''
        fn_plugin = OpenMaya.MFnPlugin(plugin)

        try: 
            fn_plugin.registerNode(
                demoNode.type_name,
                demoNode.type_id,
                demoNode.creator,
                demoNode.initialize,
                demoNode.MPxNode.kDependNode
            )
        except: 
            print('fail to initialize plugin: {0} !'.format(demoNode.type_name))

    def uninitializePlugin(plugin):
        ''' Called when the plugin is unloaded in Maya
        
        Args: 
            plug (MObject):
               the plugin to uninitialize.
        '''
        fn_plugin = OpenMaya.MFnPlugin(plugin)

        try:
            fn_plugin.deregisterNode(demoNode.type_id)
        except:  
            print('fail to initialize plugin: {0} !'.format(demoNode.type_name))

    
