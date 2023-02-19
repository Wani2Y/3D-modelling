"""
title: "**Exporting Axis Transformation of Different Joint Orientations**"
project for: "SIMM modelling"
author: "Wani2Y"
first created: "3/01/2023"
last modified: "19/02/2023"
"""

"""
Maya MMatrix is composed of a 3X3 Euler rotation matrix to represent the end concanteionus product. 
The fourth row and column are for special operations such as scale, shear. 
SIMM has a 3X3 matrix to describe joint orientation. 
Though SIMM says nothing on the manual, it does use the exact values as the Euler rotation matrix in Maya.
"""
"""
SIMM computes the distances between bones based on the parent-child connections.
To compute using values from Maya, we use the distances from the world origin (DFMO) in Maya in the following formula:
tranlation in SIMM = (DFMO of the parent) - (DFWO of the child)
"""

# import Maya scripting library for Python and access the required modules of Maya API
from maya.api.OpenMaya import MVector, MMatrix, MPoint
import maya.cmds as cmds
import csv

#first select the joint with anatomical orientation, then the world oriented one.

#create a function to calculation the transformations of MMatrix from world oriented joint to anatomical joint.
def get_trans_MMatrix (ana_joint, world_joint):
	anatomical_joint_matrix = MMatrix(cmds.xform(ana_joint, q=True, matrix=True, ws=True))
	world_joint_matrix = MMatrix(cmds.xform(world_joint, q=True, matrix=True, ws=True))
	return (anatomical_joint_matrix * world_joint_matrix.inverse())

#put seleted joints in a list
sel_bone = cmds.ls(selection=True)

#add the selected joints
#select joints in the following order (1) anatomical fo the parent, (2) anatomical of the child, and (3) world oriented
# (2) is used to compute values for mmatrix and (1) is used to compute distances between bones in SIMM
anatomical_joint = (cmds.ls(sl=1, sn=True))[1]
world_oriented_joint = (cmds.ls(sl=1, sn=True))[2]
parent_bone = cmds.xform(sel_bone[0], q=1, t=1, ws=1)
child_bone = cmds.xform(sel_bone[1], q=1, t=1, ws=1)

#store the transformation MMatrix
mmatrix_for_simm = get_trans_MMatrix(anatomical_joint, world_oriented_joint)

#change MMatrix to list for slicing
nested_list = list(mmatrix_for_simm)

#restructure the list and drop the last row and column
#round up the significant digits to 16, which is the default for SIMM
simm_joint_orientation = [
	[anatomical_joint, "x", "y", "z"],
	["order", "t", "r3", "r2", "r1"],
	["axis_1", f"{nested_list[0]:.16f}", f"{nested_list[1]:.16f}", f"{nested_list[2]:.16f}"],
	["axis_2", f"{nested_list[4]:.16f}", f"{nested_list[5]:.16f}", f"{nested_list[6]:.16f}"],
	["axis_3", f"{nested_list[8]:.16f}", f"{nested_list[9]:.16f}", f"{nested_list[10]:.16f}"],
	["tx", "constant", f"{(child_bone[0] - parent_bone[0]):.16f}"],
    ["ty", "constant", f"{(child_bone[1] - parent_bone[1]):.16f}"],
    ["tz", "constant", f"{(child_bone[2] - parent_bone[2]):.16f}"],
    ["r1", "constant",  "0.000000"],
    ["r2", "constant",  "0.000000"],
    ["r3", "constant",  "0.000000"],
]

#uncommented the following line to have a popup diaglogue windows to indicatew which .csv file to use
#filePath = cmds.fileDialog2(dialogStyle=2, fileMode =4)

#alternatively, the document is saved to the default working directory where the Maya scene is
#change eidting mode from "a" to "w" if you want to create a .csv file with the script.
with open("mmatrix.csv", "a", newline = '') as file:
	writer = csv.writer(file, delimiter = " ")
	writer.writerows(simm_joint_orientation) 