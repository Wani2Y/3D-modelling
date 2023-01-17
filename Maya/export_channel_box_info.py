"""
title: "**Exporting Translation Values of Selected Objects**"
project for: "Thesis!"
author: "Wani2Y"
first created: "10/09/2022"
last modified: "16/01/2023"
"""

# import Maya scripting library for Python
import maya.cmds as cmds

# setting the document path where the output file is created and saved
outPath = 'D:/Virtual data/muscle_landmarks.csv'

# get the coordinates of selected muscle landmarks and put them in a list
sel_obj = cmds.ls(selection=True)

# check if at least one landmark has been selected
if len(sel_obj) > 0:
    try:
        # create/open file path to write
        outFile = open(outPath, 'w')
    # return error when an incorrect directory is provided
    except:
        cmds.error('file path specified in outPath does not exist!')
else:
    cmds.warning('select at least one locator')

# remove dummy landmarks used to estiamte muscle landmarks but are not landmarks themselves
# note that this only works if multiple dummy landmarks with the same name exist, else create a blacklist to proceed
m_landmarks = []
for obj in sel_obj:
    if "|" not in obj:
        m_landmarks.append(obj)

# sort m_landmarks alphabatically
m_landmarks.sort()

# create a table to house the coordinates of muscle landmarks
m_table = ''
# put all muscle landmarks in m_table
for jnt in m_landmarks:
    m_table += jnt + ','
    # get values from the channel boxes
    pos = cmds.xform(jnt, q=1, t=1, ws=1)
    m_table += str(pos[0]) + ',' + str(pos[1]) + ',' + str(pos[2]) + ',' + '\n'

# write the data from m_table in the .csv file
outFile.write(m_table)
outFile.close()

#empty m_landmarks and sel_obj for clean operations
m_landmarks.clear()
sel_obj.clear()