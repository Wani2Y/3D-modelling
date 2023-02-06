"""
title: "**Changing rotation order of all Maya joints in the entire scene**"
project for: "Maya and SIMM modelling"
author: "Wani2Y"
first created: "06/02/2023"
last modified: "06/02/2023"
"""
"""
Maya join rotation order determines the orders in which Maya rotates X, Y, and Z axes of an object. 
This can be changed individually in the Attribute editor under Transform attributes. 
Note that rotation order is opposite to the left to righe order on the label.
For example, xyz indicates rotations starts from z to y to x. 
"""

#import Maya built-in Python functionality
import maya.cmds as cmds

#storing the joints in scene within a list
MJoint_tlist = cmds.ls(type = "joint")

#loop over all Mjoints to change the rotation order to the numeric order of the drop down list (3 for xzy)
for joint in MJoint_list:
	cmds.setAttr(joint + ".rotateOrder", 3)
