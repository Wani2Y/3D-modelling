"""
title: "**Exporting Axis Transformation of Different Joint Orientations**"
project for: "SIMM modelling"
author: "Wani2Y"
first created: "3/01/2023"
last modified: "06/02/2023"
"""

"""
Maya MMatrix is composed of a 3X3 Euler rotation matrix to represent the end concanteionus product. 
The fourth row and column are for special operations such as scale, shear. 
SIMM has a 3X3 matrix to describe joint orientation. 
Though SIMM says nothing on the manual, it does use the exact values as the Euler rotation matrix in Maya.
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

anatomical_joint = (cmds.ls(sl=1, sn=True))[0]
world_oriented_joint = (cmds.ls(sl=1, sn=True))[1]

#store the transformation MMatrix
mmatrix_for_simm = get_trans_MMatrix(anatomical_joint, world_oriented_joint)

#change MMatrix to list for slicing
nested_list = list(mmatrix_for_simm)

#restructure the list and drop the last row and column
simm_joint_orientation = [
	["joint_name", "x", "y", "z"],
	["order", "t", "r3", "r2", "r1"],
	["axis_1", nested_list[0], nested_list[1], nested_list[2]],
	["axis_2", nested_list[4], nested_list[5], nested_list[6]],
	["axis_3", nested_list[8], nested_list[9], nested_list[10]],
]

#have a popup diaglogue windows to indicatew where the .csv file is
#alternatively, the document is saved to the default working directory where the Maya scene is
#filePath = cmds.fileDialog2(dialogStyle=2, fileMode =4)

with open("mmatrix.csv", "a", newline = '') as file:
	writer = csv.writer(file, delimiter = " ")
	writer.writerows(simm_joint_orientation) 