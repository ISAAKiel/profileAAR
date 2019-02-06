# -*- coding: utf-8 -*-
from __future__ import division, print_function
from qgis.gui import QgsMessageBar
from qgis.core import *
import scipy
import sys
from math import atan, fabs, pi, cos, sin, tan, isnan, sqrt
from numpy import mean
from errorhandling import ErrorHandler
import matplotlib.pyplot as plt


def rotation (self, coord_proc, slope_deg):
    x_coord_proc = listToList(self, coord_proc, 0)
    y_coord_proc = listToList(self, coord_proc, 1)
    z_coord_proc = listToList(self, coord_proc, 2)

    # calculate the point of rotation
    center_x = mean(x_coord_proc)
    center_y = mean(y_coord_proc)
    # QgsMessageLog.logMessage(str(coord_proc[0][4]) + " " + str(center_x) + " " + str(center_y), 'MyPlugin')

    # instantiate lists for the transformed coordinates
    x_trans = []
    y_trans = []
    z_trans = []


    for i in range(len(coord_proc)):
        x_trans.append(
            center_x + (coord_proc[i][0] - center_x) * cos(slope_deg / 180 * pi) - sin(slope_deg / 180 * pi) * (
                        coord_proc[i][1] - center_y))
        y_trans.append(
            center_y + (coord_proc[i][0] - center_x) * sin(slope_deg / 180 * pi) + (coord_proc[i][1] - center_y) * cos(
                slope_deg / 180 * pi))
        z_trans.append(coord_proc[i][2])


    return {'x_trans':x_trans, 'y_trans':y_trans ,'z_trans':z_trans }

def listToList (self, coord_proc, position):
    newList = []
    for i in range(len(coord_proc)):
        newList.append(coord_proc[i][position])
    return newList

def ns_error_determination(self, coord_proc):

    xw = listToList(self, coord_proc, 0)
    yw = listToList(self, coord_proc, 1)

    # https://www.crashkurs-statistik.de/einfache-lineare-regression/
    QgsMessageLog.logMessage('xw' + str(xw) , 'error')
    QgsMessageLog.logMessage('yw' + str(yw) , 'error')
    xStrich = mean(xw)
    yStrich = mean(yw)
    QgsMessageLog.logMessage('xStrich' + str(xStrich) , 'error')
    QgsMessageLog.logMessage('yStrich' + str(yStrich) , 'error')
    abzugX = []
    abzugY = []


    for i in range(len(xw)):
        abzugX.append(xw[i] - xStrich)
        if i > 0 and xw[i] < xw[i-1]:
            x1Gerade = xw[i]
        elif i > 0 and xw[i] > xw[i-1]:
            x2Gerade = xw[i]
        elif i == 0:
            x1Gerade = xw[i]
            x2Gerade = xw[i]

    QgsMessageLog.logMessage('x1Gerade' + str(x1Gerade) , 'error')
    QgsMessageLog.logMessage('x2Gerade' + str(x2Gerade) , 'error')
    QgsMessageLog.logMessage('abzugX' + str(abzugX) , 'error')

    for i in range(len(yw)):
        QgsMessageLog.logMessage('ps' + str(i), 'yy')
        QgsMessageLog.logMessage('yyy' + str(yw[i]), 'yy')

        if i > 0 and yw[i] < ymin:
            ymin = yw[i]
            ymin_postition = i
        elif i > 0 and yw[i] > ymax:

            ymax = yw[i]
            ymax_postition = i
        elif i == 0:
            ymin = yw[i]
            ymin_postition = i
            ymax = yw[i]
            ymax_postition = i
        abzugY.append(yw[i] - yStrich)


    QgsMessageLog.logMessage('ymax' + str(ymax) , 'error')
    QgsMessageLog.logMessage('ymin' + str(ymin) , 'error')
    QgsMessageLog.logMessage('abzugY' + str(abzugY) , 'error')
    QgsMessageLog.logMessage('ymin_postition' + str(ymin_postition) , 'error')
    QgsMessageLog.logMessage('ymax_postition' + str(ymax_postition) , 'error')


    abzugXsum =  0
    abzugXsum2 = 0


    for i in range(len(abzugX)):
        abzugXsum = abzugXsum + abzugX[i] * abzugY[i]
        abzugXsum2 = abzugXsum2 + abzugX[i] * abzugX[i]


    QgsMessageLog.logMessage('abzugXsum' + str(abzugXsum) , 'error')
    QgsMessageLog.logMessage('abzugXsum2' + str(abzugXsum2) , 'error')

    b = abzugXsum / abzugXsum2
    a = yStrich - b * xStrich

    QgsMessageLog.logMessage('a' + str(a) , 'error')
    QgsMessageLog.logMessage('b' + str(b) , 'error')

    y1Gerade = a + b * x1Gerade
    y2Gerade = a + b * x2Gerade

    QgsMessageLog.logMessage('y1Gerade' + str(y1Gerade) , 'error')
    QgsMessageLog.logMessage('y2Gerade' + str(y2Gerade) , 'error')

    steigung_neu = atan((y2Gerade - y1Gerade) / (x2Gerade - x1Gerade)) * 180 / pi
    #Falls das Profil perfekt o-w ausgerichtet ist, ist alles ok

    try:
        steigung_alt = atan((ymax - ymin) / (xw[ymax_postition] - xw[ymin_postition])) * 180 / pi
    except ZeroDivisionError:
        steigung_alt = steigung_neu

    QgsMessageLog.logMessage('ymax - ymin' + str(ymax - ymin) , 'error1')
    QgsMessageLog.logMessage('xw[ymax_postition] - xw[ymin_postition]' + str(xw[ymax_postition] - xw[ymin_postition]) , 'error1')

    QgsMessageLog.logMessage('steigung_neu' + str(steigung_neu) , 'error')
    QgsMessageLog.logMessage('steigung_alt' + str(steigung_alt) , 'error')
    QgsMessageLog.logMessage('steigung_alt round' + str(abs(round(steigung_alt, 0))), 'error')

    pluszehn = abs(steigung_alt) + (abs(steigung_alt) * 10 / 100)
    minuszehn = abs(steigung_alt) - (abs(steigung_alt) * 10 / 100)

    if abs(steigung_neu) > pluszehn and abs(round(steigung_alt, 0)) != 45 or  abs(steigung_neu) < minuszehn and abs(round(steigung_alt, 0)) != 45:
        return bool(True)
    else:
        return bool(False)




def list_column_zero(listsort, column):
    for points in range(len(listsort)):
        listsort[points][column] = 0
    return listsort

def list_add_rowcount_to_column(listsort):
    for points in range(len(listsort)):
        listsort[points].append(points)
    return  listsort

def list_plus_rowcount_to_column(listsort, column):
    for points in range(len(listsort)):
        listsort[points][column] = listsort[points][column] + points
    return listsort

#change
def check_original_steigung(original_outer_points):
    # Check the Slope of the outer points, if it´s too close to a S-N orientation rotate the points
    slope_original_outer_points = (original_outer_points[1][1] - original_outer_points[0][1]) / (
                original_outer_points[1][0] - original_outer_points[0][0])
    if slope_original_outer_points > 0:
        steigung_original_outer_points = atan(slope_original_outer_points)
        return steigung_original_outer_points
    elif slope_original_outer_points < 0:
        steigung_original_outer_points = atan(slope_original_outer_points) + 180
        return steigung_original_outer_points
    else:
        steigung_original_outer_points = 90
        return steigung_original_outer_points


class Magic_Box:
    def __init__(self, qgisInterface):
        self.qgisInterface = qgisInterface

    def transformation(self, coord_proc, method, direction):
        #initialize the Errorhandler
        errorhandler = ErrorHandler(self)
        profilnr_proc = listToList(self, coord_proc, 4)

        fehler_check = False
        ns_fehler_vorhanden = ns_error_determination(self, coord_proc)
        if ns_fehler_vorhanden:
            QgsMessageLog.logMessage('Pr' + str(profilnr_proc), 'Kackprofil')
            # Profil um 45 Grad drehen
            rotationresult = rotation(self, coord_proc, 45)
            fehler_check = True
            for i in range(len(coord_proc)):
                coord_proc[i][0] = rotationresult['x_trans'][i]
                QgsMessageLog.logMessage(str(coord_proc[i][0]), 'x')
                coord_proc[i][1] = rotationresult['y_trans'][i]
                QgsMessageLog.logMessage(str(coord_proc[i][1]), 'y')
                coord_proc[i][2] = rotationresult['z_trans'][i]

        #write the x and v values in the corresponding lists

        # instantiate an empty list for the transformed coordinates and other values
        # instantiate lists for the x and y values
        x_coord_proc = listToList(self, coord_proc, 0)
        y_coord_proc = listToList(self, coord_proc, 1)
        z_coord_proc = listToList(self, coord_proc, 2)
        selection_proc = listToList(self, coord_proc, 5)

        id_proc = listToList(self, coord_proc, 6)
        rangcheck_orginal = []


        for i in range(len(coord_proc)):

            tmplist = []
            for k in range(len(coord_proc[i])):
                tmplist.append(coord_proc[i][k])
            rangcheck_orginal.append(tmplist)

        for coords in range(len(rangcheck_orginal)):
            del rangcheck_orginal[coords][5]
            del rangcheck_orginal[coords][4]
            del rangcheck_orginal[coords][3]
        #distanz zwischen den beiden Punkten oben CHANGE



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



        if isnan(res_y) or res_x >= res_y:
            linegress = linegress_x
            slope = linegress[0]
        elif isnan(res_x) or res_x < res_y:
             linegress = linegress_y
             # if the linear regression with the changed values was used, the angle of the slope is rotated by 90°
             slope = tan((-90-(((atan(linegress[0])*180)/pi)))*pi / 180)
        else:
            self.qgisInterface.messageBar().pushMessage("Error", "Calculation failed! Corrupt data!",
                                                        level=QgsMessageBar.CRITICAL)
            sys.exitfunc()





        #CHANGE Check the distance with all points
        #TODO Testen
        distance = errorhandler.calculateError(linegress, xw_check, yw_check, coord_proc[0][4])

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
        #CHANGE
        rangcheck_trans = []
        # build the finished list
        for i in range(len(coord_proc)):
            #CHANGE
            coord_trans.append([x_trans[i], y_trans[i], z_trans[i], coord_proc[i][4], coord_proc[i][2], distance[i], selection_proc[i], id_proc[i]])
            rangcheck_trans.append([x_trans[i], z_trans[i], y_trans[i]])
      
        #If the aim is to get the view of the surface, the x-axis has to be rotated aswell
        if method == "surface":
            # calculating the slope, therefore preparing lists
            z_yw = []
            z_zw = []
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
            rangcheck_trans = []
            for i in range(len(coord_proc)):
                # CHANGE
                coord_trans.append([x_trans[i], y_trans[i], z_trans[i], coord_proc[i][4], coord_proc[i][2], distance[i], selection_proc[i],id_proc[i]])
                rangcheck_trans.append([x_trans[i], z_trans[i], y_trans[i]])

        # If the direction is in the "original" setting, the points have to be rotated back to their original orientation
        if direction == "original":
            # the rotation angle is the negative angle of the first rotation
            QgsMessageLog.logMessage('Fehler:' + str(fehler_check), 'Fehle')
            if fehler_check == True:
                y_slope_deg = -slope_deg - 45
                QgsMessageLog.logMessage('Fehler:' + str('1'), 'Fehle')
            else:
                y_slope_deg = -slope_deg
                QgsMessageLog.logMessage('Fehler:' + str('2'), 'Fehle')

            # get the centerpoint
            y_center_x = mean(x_trans)
            y_center_z = mean(z_trans)

            #rewrite the lists for the x and z values
            x_trans = []
            z_trans = []
            for i in range(len(coord_trans)):
                x_trans.append(y_center_x + (coord_trans[i][0] - y_center_x) * cos(y_slope_deg / 180 * pi) - (coord_trans[i][2] - y_center_z)
                               * sin(y_slope_deg / 180 * pi))
                z_trans.append(y_center_z + (coord_trans[i][0] - y_center_x) * sin(y_slope_deg / 180 * pi) + (coord_trans[i][2] - y_center_z)
                               * cos(y_slope_deg / 180 * pi))

            # empty and rewrite the output list
            coord_trans = []
            rangcheck_trans = []
            for i in range(len(coord_proc)):
                # CHANGE
                coord_trans.append([x_trans[i], y_trans[i], z_trans[i], coord_proc[i][4], coord_proc[i][2], distance[i], selection_proc[i], id_proc[i]])
                rangcheck_trans.append([x_trans[i], z_trans[i], y_trans[i]])



        #change

        # check the distances of the outter points from the old points and the converted ones
        original_outer_points = self.outer_profile_points(coord_proc)
        original_distance = self.calculate_distance_from_outer_profile_points_orgiginal(original_outer_points)

        new_outer_points = []
        for point in coord_trans:
            QgsMessageLog.logMessage('PUUUNKT' + str(point[7]))
            if point[7] == original_outer_points[0][6] or point[7] == original_outer_points[1][6]:
                new_outer_points.append(point)
        new_distance = self.calculate_distance_from_outer_profile_points_proc(new_outer_points)



        QgsMessageLog.logMessage('PR:' + str(coord_proc[0][4]), 'Distance')
        #QgsMessageLog.logMessage('slope: ' + str(slope_deg), 'Distance')
        QgsMessageLog.logMessage('Original Distance: ' + str(original_distance), 'Distance')
        #new_distance = calculate_distance_new(rangcheck_trans)
        QgsMessageLog.logMessage('New Distance: ' + str(new_distance), 'Distance')
        QgsMessageLog.logMessage('Diff. Distance: ' + str(abs(original_distance-new_distance)), 'Distance')




        if abs(original_distance - new_distance) > 0.01:
            self.qgisInterface.messageBar().pushMessage("Error",
                                                       "Profile was calculated incorrect (1cm acc.) See Log-Window: " + str(
                                                           str(coord_proc[0][4])),
                                                       level=QgsMessageBar.CRITICAL)
            QgsMessageLog.logMessage('PR:' + str(coord_proc[0][4]), 'Distance > 1cm')
            QgsMessageLog.logMessage('slope: ' + str(slope_deg), 'Distance > 1cm')
            QgsMessageLog.logMessage('Original Distance: ' + str(original_distance), 'Distance > 1cm')
            QgsMessageLog.logMessage('New Distance: ' + str(new_distance), 'Distance > 1cm')
            QgsMessageLog.logMessage('Diff. Distance: ' + str(abs(original_distance - new_distance)), 'Distance > 1cm')
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

    def outer_profile_points(self, coords):
        # get the two points with the highest and lowest xvalue
        coords_sorted = sorted(coords, key=lambda x: (x[0]))
        two_lowest = coords_sorted[:2]
        two_highest = coords_sorted[-2:]
        #QgsMessageLog.logMessage("two_lowest: " + str(two_lowest), 'MyPlugin')
        #QgsMessageLog.logMessage("two_highest: " + str(two_highest), 'MyPlugin')
        #check which one of the points has the higher z value and write it into a variable
        if two_lowest[1][2] > two_lowest[0][2]:
            lowestx = two_lowest[1]
        else:
            lowestx = two_lowest[0]
        if two_highest[1][2] > two_highest[0][2]:
            highestx = two_highest[1]
        else:
            highestx = two_highest[0]
        return [lowestx, highestx]

    def calculate_distance_from_outer_profile_points_orgiginal(self, outer_points):
        distance = sqrt((outer_points[1][0]-outer_points[0][0])**2 + (outer_points[1][1]-outer_points[0][1])**2)
        return distance

    def calculate_distance_from_outer_profile_points_proc(self, outer_points):
        distance = sqrt((outer_points[1][0]-outer_points[0][0])**2 + (outer_points[1][2]-outer_points[0][2])**2)
        return distance


    def calculateResidual(self, linegress, array1, array2, prnr):
        # This calculates the predicted value for each observed value
        obs_values = array2
        pred_values = linegress[0] * array1 + linegress[1]

        # This prints the residual for each pair of observations
        Residual = obs_values - pred_values

        return sum(Residual)




































