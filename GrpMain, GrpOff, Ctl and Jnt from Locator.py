import maya.cmds as cmds

class CreateAndRenameWindow(object):
    windowName = "CreateAndRenameWindow"
    instance = None

    @classmethod
    def show(cls):
        if cls.instance:
            cmds.deleteUI(cls.windowName, window=True)

        cls.instance = CreateAndRenameWindow()
        cls.instance.create()

    def create(self):
        self.window = cmds.window(self.windowName)
        self.buildUI()
        cmds.showWindow(self.window)

    def buildUI(self):
        column = cmds.columnLayout(adjustableColumn=True)
        cmds.text(label='Enter new names:')
        self.groupMainNameField = cmds.textField(placeholderText='Group Main name')
        self.groupOffNameField = cmds.textField(placeholderText='Group Offset name')
        self.controlNameField = cmds.textField(placeholderText='Control name')
        self.jointNameField = cmds.textField(placeholderText='Joint name')
        cmds.button(label='Create and Rename', command=self.createAndRename)

    def createAndRename(self, *args):
        groupMainNewName = cmds.textField(self.groupMainNameField, query=True, text=True)
        groupOffName = cmds.textField(self.groupOffNameField, query=True, text=True)
        controlNewName = cmds.textField(self.controlNameField, query=True, text=True)
        jointNewName = cmds.textField(self.jointNameField, query=True, text=True)

        locatorTransform = cmds.ls(selection=True, type='transform')
        shapes = cmds.listRelatives(locatorTransform, shapes=True)
        if not shapes or 'locator' not in cmds.nodeType(shapes[0]):
            cmds.warning('No locator selected.')
            return

        locatorPos = cmds.xform(locatorTransform[0], query=True, worldSpace=True, translation=True)

        # Create the joint, control, and group
        joint = cmds.joint(name=jointNewName)
        control = cmds.circle(name=controlNewName, normal=(0, 1, 0))[0]
        groupMain = cmds.group(empty=True, name=groupMainNewName)
        groupOff = cmds.group(empty=True, name=groupOffName)

        # Position the group at the locator's position
        cmds.xform(groupMain, worldSpace=True, translation=locatorPos)
        cmds.xform(groupOff, worldSpace=True, translation=locatorPos)
        cmds.xform(control, worldSpace=True, translation=locatorPos)
        cmds.xform(joint, worldSpace=True, translation=locatorPos)


        # Parent the joint to the control, and the control to the group
        cmds.parent(joint, control)
        cmds.parent(control, groupOff)
        cmds.parent(groupOff, groupMain)

        # Reset the transformations of the joint and control
        cmds.xform(joint, objectSpace=True, translation=(0, 0, 0))
        cmds.xform(control, objectSpace=True, translation=(0, 0, 0))
        cmds.parent(joint,world=True)
        
        
        
CreateAndRenameWindow.show()
