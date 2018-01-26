# -*- coding: utf-8 -*-
from __future__ import division, print_function
from qgis.gui import QgsMessageBar
from qgis.core import *
import scipy
import sys
from math import atan, fabs, pi, cos, sin, tan
from numpy import mean
from errorhandling import ErrorHandler
import matplotlib.pyplot as plt


def testplot(self, xw, yw, linegress, prnr):
    if (prnr == "8" or prnr == "53" or prnr == "37" or prnr == "1"):
        intercept = linegress[1]
        slope = linegress[0]
        neu_y = []
        neu_x = []

        for coords in range(len(xw)):
            neu_y.append(slope * xw[coords] + intercept)
        for coords in range(len(yw)):
            neu_x.append(slope * yw[coords] + intercept)
        QgsMessageLog.logMessage(str(xw), 'test')
        plt.plot(xw,yw, 'o', label='original data PR' + str(prnr))
        plt.plot(xw, neu_y, 'r', label='fitted line_1')
        plt.plot(neu_x, yw, 'b', label='fitted line_2')
        #plt.plot(xw, intercept + slope * xw, 'o', label='fitted points')
        plt.legend()
        plt.show()


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
        selection_proc = []
        profilnr_proc =[]
        # write the x and v values in the corresponding lists
        for i in range(len(coord_proc)):
            x_coord_proc.append(coord_proc[i][0])
            y_coord_proc.append(coord_proc[i][1])
            z_coord_proc.append(coord_proc[i][2])
            #CHANGE
            selection_proc.append(coord_proc[i][5])
            profilnr_proc.append(coord_proc[i][4])

        # create the valuelists that are used
		#EINFUEGEN WENN Spalte = x verwenden
        xw = []
        yw = []
        #CHANGE
        xw_check = []
        yw_check = []
        for x in range(len(x_coord_proc)):
            #CHANGE Nur Auswahl zum berechnen der Steigung verwenden
            if(selection_proc[x] == 1):
                xw.append(x_coord_proc[x] - min(x_coord_proc))
                yw.append(y_coord_proc[x] - min(y_coord_proc))
            xw_check.append(x_coord_proc[x] - min(x_coord_proc))
            yw_check.append(y_coord_proc[x] - min(y_coord_proc))

        #QgsMessageLog.logMessage(str(xw), 'MyPlugin')
        #CHANGE
        #There is a problem with lingress if the points are nearly N-S oriented
        #To solve this, it is nessecary to change the input values of the regression
        # Calculate the regression for both directions
        linegress_x = scipy.stats.linregress(scipy.array(xw), scipy.array(yw))
        linegress_y = scipy.stats.linregress(scipy.array(yw), scipy.array(xw))
        # get the sum of residuals for both direction
        #We like to use the regression with less sum of the residuals
        
        res_x = self.calculateResidual(linegress_x, scipy.array(xw), scipy.array(yw), profilnr_proc[0])
        res_y = self.calculateResidual(linegress_y, scipy.array(yw), scipy.array(xw), profilnr_proc[0])
        QgsMessageLog.logMessage(str(profilnr_proc[0]), 'methode')
        if lingress_x is not None and res_x >= res_y:
            linegress = linegress_x
            slope = linegress[0]
            QgsMessageLog.logMessage(str("1"), 'methode')
        elif lingress_x is None or res_x < res_y:
             linegress = linegress_y
             # if the linear regression with the changed values was used, the angle of the slope is rotated by 90°
             slope = tan((-90-(((atan(linegress[0])*180)/pi)))*pi / 180)
             QgsMessageLog.logMessage(str("2"), 'methode')
        else:
            self.qgisInterface.messageBar().pushMessage("Error", "Calculation failed! Corrupt data!",
                                                        level=QgsMessageBar.CRITICAL)
            sys.exitfunc()



        #CHANGE Check the distance with all points
        distance = errorhandler.calculateError(linegress, xw_check, yw_check, coord_proc[0][4])
        QgsMessageLog.logMessage(str(coord_proc[0][4]), 'linegress')
        QgsMessageLog.logMessage(str(linegress[3]), 'linegress')
        QgsMessageLog.logMessage(str(linegress[4]), 'linegress')
        if (linegress[4] > 1):
            QgsMessageLog.logMessage(str(coord_proc[0][4]), 'scheisse')
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

        #if slope > 0 and slope < 1 and coord_proc[0][3] in ["E"]:
        #    slope_deg = 90
        #    QgsMessageLog.logMessage(str(profilnr_proc[0]), 'sonderfall')
        #if (profilnr_proc[0] == '8' or profilnr_proc[0] == '37' ):
        #    QgsMessageLog.logMessage(str(profilnr_proc[0]), 'steigung')
        #    QgsMessageLog.logMessage(str(slope), 'steigung')
        #    QgsMessageLog.logMessage(str((atan(slope) * 180) / pi), 'steigung')


        testplot(self, xw, yw, linegress, profilnr_proc[0])
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
            #CHANGE
            coord_trans.append([x_trans[i], y_trans[i], z_trans[i], coord_proc[i][4], coord_proc[i][2], distance[i], selection_proc[i]])
       
      
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
                # CHANGE
                coord_trans.append([x_trans[i], y_trans[i], z_trans[i], coord_proc[i][4], coord_proc[i][2], distance[i], selection_proc[i]])

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
                # CHANGE
                coord_trans.append([x_trans[i], y_trans[i], z_trans[i], coord_proc[i][4], coord_proc[i][2], distance[i], selection_proc[i]])

        return coord_trans

    #CHANGE NEW
    def height_points (self, coord_trans):
        #Getting the top right point and export it to a pointshape
        xw = []
        yw = []
        height_point = []
        upperright_last = 0
        for i in range(len(coord_trans)):
            upperright_check = coord_trans[i][0] + coord_trans[i][2]
            if upperright_check > upperright_last:
                upperright_last = upperright_check
                height_point = coord_trans[i]
        return height_point




    def calculateResidual(self, linegress, array1, array2, prnr):
        # This calculates the predicted value for each observed value
        obs_values = array2
        pred_values = linegress[0] * array1 + linegress[1]

        # This prints the residual for each pair of observations
        Residual = obs_values - pred_values
        if (prnr == "1" or prnr == "8" or prnr == "37"):
            QgsMessageLog.logMessage('PR:'+ str(prnr)+' res: '+str(sum(Residual)), 'residual')
        return sum(Residual)




































