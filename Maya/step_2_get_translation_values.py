"""
title: "**Exporting Axis Transformation of Different Joint Orientations**"
project for: "SIMM modelling"
author: "Wani2Y"
first created: "06/02/2023"
last modified: "06/02/2023"
"""

"""
SIMM computes the distances between bones based on the parent-child connections.
To compute using values from Maya, we use the distances from the world origin (DFMO) in Maya in the following formula:
tranlation in SIMM = (DFMO of the parent) - (DFWO of the child)
"""

# import Maya scripting library for Python
import maya.cmds as cmds
import csv

# translate both parent and child bones to the world origin. Then first select the parent bone and then the child bone
sel_bone = cmds.ls(selection=True)

# get the distances from the origin for both parent and child bones
parent_bone = cmds.xform(sel_bone[0], q=1, t=1, ws=1)
child_bone = cmds.xform(sel_bone[1], q=1, t=1, ws=1)

# create a lsit in the same format as the SIMM joint file
simm_joint_translation = [
    ["tx", parent_bone[0] - child_bone[0]],
    ["ty", parent_bone[1] - child_bone[1]],
    ["tz", parent_bone[2] - child_bone[2]],
    ["r1", "constant",  "0.000000"],
    ["r2", "constant",  "0.000000"],
    ["r3", "constant",  "0.000000"],
]

#have a popup diaglogue windows to indicatew where the .csv file is
#alternatively, the document is saved to the default working directory where the Maya scene is
#filePath = cmds.fileDialog2(dialogStyle=2, fileMode =4)

with open("mmatrix.csv", "a", newline = '') as file:
	writer = csv.writer(file, delimiter = " ")
	writer.writerows(simm_joint_translation) 