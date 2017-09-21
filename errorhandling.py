# -*- coding: utf-8 -*-
"""
/***************************************************************************
 profileAARDialog
                                 A QGIS plugin
 profileAAR des
                             -------------------
        begin                : 2017-08-31
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Moritz Mennenga / Kay Schmütz / Christoph Rinne
        email                : mennenga@nihk.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.gui import QgsMessageBar
from qgis.core import *
from numpy import std, mean
import sys
from math import pi, fabs
import matplotlib.pyplot as plt
import scipy

#columreader in a "table" (list of lists)
def columnreader(list_in_list_object, columnindex):
    columnvalues = []
    for i in range(len(list_in_list_object)):
        columnvalues.append(list_in_list_object[i][columnindex])
    return columnvalues

class ErrorHandler:
    def __init__(self, qgisInterface):
        self.qgisInterface = qgisInterface

#Checks that have to do on every single Profile
    def singleprofile(self, coord_proc, view_check, profile_name):
        # TODO: check for consistency before calculation
        # TODO: check for spatial consistency (no points should be more than x meters apart)
        
        # check if actual profile has less then 4 points
        if len(coord_proc) <= 3:
            #if it is less, print error message
            self.qgisInterface.messageBar().pushMessage("Error", "A profile needs min. 4 points. Error on profile: "+str(profile_name), level=QgsMessageBar.CRITICAL)
            #cancel execution of the script
            sys.exitfunc()

        # check if the view value is the same in all features
        if len(view_check) != 1:
            # if it is not the same, print error message
            self.qgisInterface.messageBar().pushMessage("Error", "The view column of your data is inconsistant (either non or two different views are present). Error on profile: " + str(profile_name), level=QgsMessageBar.CRITICAL)
            # cancel execution of the script
            sys.exitfunc()

        # check if the view is one of the four cardinal directions
        if view_check[0].upper() not in ["N", "E", "S", "W"]:
            # if it is not the same, print error message
            self.qgisInterface.messageBar().pushMessage("Error", "The view value is not one of the four cardinal directions. Error on profile: " + str(profile_name), level=QgsMessageBar.CRITICAL)
            # cancel execution of the script
            sys.exitfunc()

        # check if the coordinates x, y, z fall into 2 sigma range
        #instance a table like list of lists with i rows and j columns
        warning_message = []
        for i in range(3):
            xyz = []
            xyz_lower = []
            xyz_upper = []
            xyz = columnreader(coord_proc, i)
            xyz_lower = mean(xyz) - (2 * std(xyz))
            xyz_upper = mean(xyz) + (2 * std(xyz))
            for j in range(len(xyz)):
                if xyz[j] < xyz_lower or xyz[j] > xyz_upper:
                    QgsMessageLog.logMessage('Range profile ' + str(profile_name) + ': ' + str(xyz_lower) + " - " + str(xyz_upper), 'profileAAR')
                    QgsMessageLog.logMessage('value ' + str(xyz[j]), 'MyPlugin')
                    #warning_message.append("Warning: Profile " )+ str(profile_name) + chr(120+i) + str(j) + 'excedes th 2 std interval of ' + chr(120+i))
                    self.qgisInterface.messageBar().pushMessage("Warning: Profile " + str(profile_name) +': '+ chr(120+i) + 'Pt ' + str(j+1) + ' exceeds the 2std interval of ' + chr(120+i))
        #self.qgisInterface.messageBar().pushMessage('\n'.join(warning_message), level=QgsMessageBar.INFO)

#general checks for the fields of the layer after the import
    def field_check (self, layer, z_field):
        #Check if the vectorlayer is projected
        if layer.crs().geographicFlag() == True:
            self.qgisInterface.messageBar().pushMessage("Information", "Layer "+layer.name()+ " is not projected. Please choose an projected reference system.", level=QgsMessageBar.CRITICAL)
            # cancel execution of the script
            sys.exitfunc()
            
        #check the z-field
        for field in layer.fields():
            #Take a look for the z Field
            if str(field.name()) == str(z_field):
                # if the z value is not a float
                if field.typeName() != "Real" and field.typeName() != "double":
                    #Give a message
                    self.qgisInterface.messageBar().pushMessage("Error", "The z-Value needs to be a float. Check the field type of the z-Value", level=QgsMessageBar.CRITICAL)
                    # cancel execution of the script
                    sys.exitfunc()
        


#checks if the inputfields are filled correct
    def input_check(self, value):
        if str(value) == "":
            self.qgisInterface.messageBar().pushMessage("Error", "Please choose an output file!", level=QgsMessageBar.CRITICAL)
            # cancel execution of the script
            sys.exitfunc()
            

    def result_check (self, coord_trans):
        #for checking the accuracy of the points we create an line throught the profile. (Do it the easy way: y-value of a point - mean y-Value)
        #the distances from each point to the profile will lead to a comparable number
        #mean value of all Y values
        ymean = mean(columnreader(coord_trans,1))
        #list for the result
        check_result = []
        #go throught the profile
        for i in range(len(coord_trans)):
            #calculate for each point the absolute distance to a virtual line that is parallel to the x axis in the middle of the profile
            check_result.append(fabs(coord_trans[i][1]- ymean))
        #print the min max and mean values
        QgsMessageLog.logMessage('Profile:' + str(coord_trans[0][3]), 'profileAAR')
        QgsMessageLog.logMessage('Y-Error min:' + str(round(min(check_result),2)), 'profileAAR')
        QgsMessageLog.logMessage('Y-Error mean:' + str(round(mean(check_result),2)), 'profileAAR')
        QgsMessageLog.logMessage('Y-Error max:' + str(round(max(check_result),2)), 'profileAAR')
        QgsMessageLog.logMessage(' ', 'profileAAR')        