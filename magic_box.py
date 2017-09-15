# -*- coding: utf-8 -*-
from __future__ import division, print_function
from qgis.gui import QgsMessageBar
from qgis.core import *
import scipy
from math import atan, fabs, pi, cos, sin
from numpy import mean

class Magic_Box:
    def __init__(self, qgisInterface):
        self.qgisInterface = qgisInterface

    def transformation(self, coord_proc):
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
        slope = scipy.stats.linregress(scipy.array(xw), scipy.array(yw))[0]
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

        # TODO: Optionen mit übernehmen und Script weiter übersetzen - Kay


        return coord_trans


































