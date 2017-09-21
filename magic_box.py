# -*- coding: utf-8 -*-
from __future__ import division, print_function
from qgis.gui import QgsMessageBar
from qgis.core import *
import scipy
from math import atan, fabs, pi, cos, sin
from numpy import mean
from errorhandling import ErrorHandler

class Magic_Box:
    def __init__(self, qgisInterface):
        self.qgisInterface = qgisInterface

    def transformation(self, coord_proc, method, direction):
        #initialize the Errorhandler
        errorhandler = ErrorHandler(self)
        # instantiate an empty list for the transformed coordinates and other values
        coord_trans = []
        # instantiate lists for the x and y values
        x_coord_proc = []
        y_coord_proc = []
        z_coord_proc = []
        # write the x and v values in the corresponding lists
        for i in range(len(coord_proc)):
            x_coord_proc.append(coord_proc[i][0])
            y_coord_proc.append(coord_proc[i][1])
            z_coord_proc.append(coord_proc[i][2])

        # create the valuelists that are used
        xw = []
        yw = []
        for x in range(len(x_coord_proc)):
            xw.append(x_coord_proc[x] - min(x_coord_proc))
            yw.append(y_coord_proc[x] - min(y_coord_proc))

        #QgsMessageLog.logMessage(str(xw), 'MyPlugin')

        # calculate the slope of the profile using a linear regression
        linegress = scipy.stats.linregress(scipy.array(xw), scipy.array(yw))
        
        QgsMessageLog.logMessage("Stderr Profile: "+str(coord_proc[0][4]) + " MinResiduals: " + str(linegress[4]) ,'profileAAR')
        errorhandler.linreg_residuals(scipy.array(xw), scipy.array(yw),coord_proc[0][4])        
        #get the slope
        slope =linegress[0]
        # QgsMessageLog.logMessage(str(slope), 'MyPlugin')

        # calculate the degree of the slope
        slope_deg = 0.0
        if slope < 0 and coord_proc[0][3] in ["N", "E"]:
            slope_deg = 180 - fabs((atan(slope)*180)/pi) * -1
        elif slope < 0 and coord_proc[0][3] in ["S", "W"]:
            slope_deg = fabs((atan(slope) * 180) / pi)
        elif slope > 0 and coord_proc[0][3] in ["S", "E"]:
            slope_deg = ((atan(slope) * 180) / pi) * -1
        elif slope > 0 and coord_proc[0][3] in ["N", "W"]:
            slope_deg = 180 - ((atan(slope) * 180) / pi)
        elif slope == 0 and coord_proc[0][3] == "N":
            slope_deg = 180

            #QgsMessageLog.logMessage(str(coord_proc[0][4]) + " " + str(slope) + " " + str(slope_deg), 'MyPlugin')

        # calculate the point of rotation
        center_x = mean(x_coord_proc)
        center_y = mean(y_coord_proc)
        #QgsMessageLog.logMessage(str(coord_proc[0][4]) + " " + str(center_x) + " " + str(center_y), 'MyPlugin')

        # instantiate lists for the transformed coordinates
        x_trans = []
        y_trans = []
        z_trans = []

        for i in range(len(coord_proc)):
            x_trans.append(center_x + (coord_proc[i][0] - center_x) * cos(slope_deg / 180 * pi) - sin(slope_deg / 180 * pi) * (coord_proc[i][1] - center_y))
            y_trans.append(center_y + (coord_proc[i][0] - center_x) * sin(slope_deg / 180 * pi) + (coord_proc[i][1] - center_y) * cos(slope_deg / 180 * pi))
            z_trans.append(coord_proc[i][2] + center_y - mean(z_coord_proc))

        # instantiate a list for the transformed coordinates
        coord_trans = []

        # build the finished list
        for i in range(len(coord_proc)):
            coord_trans.append([x_trans[i], y_trans[i], z_trans[i], coord_proc[i][4]])

        #If the aim is to get the view of the surface, the x-axis has to be rotated aswell
        if method == "surface":
            # calculating the slope, therefore preparing lists
            z_yw = []
            z_zw =[]
            for i in range(len(coord_proc)):
                z_yw.append(y_trans[i] - min(y_trans + z_trans))
                z_zw.append(z_trans[i] - min(y_trans + z_trans))

            # actual calculation of the slope using the linear regression again
            z_slope = scipy.stats.linregress(scipy.array(z_yw), scipy.array(z_zw))[0]

            # transform the radians of the slope into degrees
            z_slope_deg = 0.0
            if z_slope < 0:
                z_slope_deg = -(90 -fabs(((atan(z_slope) * 180) / pi)))
            elif z_slope > 0:
                z_slope_deg = 90 - ((atan(z_slope) * 180)/pi)
            elif z_slope == 0:
                z_slope_deg = 0.0

            # calculate the centerpoint
            z_center_y = mean(y_trans)
            z_center_z = mean(z_trans)

            # rewrite the lists for the y and z values
            y_trans = []
            z_trans = []
            for i in range(len(coord_trans)):
                y_trans.append(z_center_y + (coord_trans[i][1] - z_center_y) * cos(z_slope_deg / 180 * pi) - (coord_trans[i][2] - z_center_z) * sin(z_slope_deg / 180 * pi))
                z_trans.append(z_center_z + (coord_trans[i][1] - z_center_y) * sin(z_slope_deg / 180 * pi) + (coord_trans[i][2] - z_center_z) * cos(z_slope_deg / 180 * pi))

            # empty and rewrite the output list
            coord_trans = []
            for i in range(len(coord_proc)):
                coord_trans.append([x_trans[i], y_trans[i], z_trans[i], coord_proc[i][4]])

        # If the direction is in the "original" setting, the points have to be rotated back to their original orientation
        if direction == "original":
            # the rotation angle is the negative angle of the first rotation
            y_slope_deg = -slope_deg

            # get the centerpoint
            y_center_x = mean(x_trans)
            y_center_z = mean(z_trans)

            #rewrite the lists for the x and z values
            x_trans = []
            z_trans = []
            for i in range(len(coord_trans)):
                x_trans.append(y_center_x + (coord_trans[i][0] - y_center_x) * cos(y_slope_deg / 180 * pi) - (coord_trans[i][2] - y_center_z) * sin(y_slope_deg / 180 * pi))
                z_trans.append(y_center_z + (coord_trans[i][0] - y_center_x) * sin(y_slope_deg / 180 * pi) + (coord_trans[i][2] - y_center_z) * cos(y_slope_deg / 180 * pi))

            # empty and rewrite the output list
            coord_trans = []
            for i in range(len(coord_proc)):
                coord_trans.append([x_trans[i], y_trans[i], z_trans[i], coord_proc[i][4]])


        return coord_trans


































