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

'''
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
        plt.plot(xw,yw, 'o', label='original data PR' + str(prnr))
        plt.plot(xw, neu_y, 'r', label='fitted line_1')
        plt.plot(neu_x, yw, 'b', label='fitted line_2')
        #plt.plot(xw, intercept + slope * xw, 'o', label='fitted points')
        plt.legend()
        plt.show()


def calculate_distance_new(coord_proc):
    # x y z (rang)

    # Ranking für jeden Punkt ermitteln
    # dazu werte nach x sortieren
    listsort_x = sorted(coord_proc, key=lambda x: (x[0]))
    # Dann für jeden Punkt den Rang dazuschrieben
    list_add_rowcount_to_column(listsort_x)
    #testgeloet
    teststring = ""
    for value in listsort_x:
        teststring += str(value) + ", "

    QgsMessageLog.logMessage('CalcDistNew: listsort_X1' + teststring)
    # ende

    # nach y sortieren und den Rang hinzufuegen
    listsort_x = sorted(listsort_x, key=lambda x: (x[1]))
    list_plus_rowcount_to_column(listsort_x, 3)
    #testgeloet
    teststring = ""
    for value in listsort_x:
        teststring += str(value) + ", "
    QgsMessageLog.logMessage('CalcDistNew: listsort_X2' + teststring)
    #ende

    # jetzt die liste nach Rang sortieren
    # die Werte mit dem höchsten Rang sind die oben.
    # Falls zwei Werte den gleichen Rang haben, ist es der mit dem höheren z wert
    listsort_x = sorted(listsort_x, key=lambda x: (-x[3], x[2]))
    koordinate2 = listsort_x[0]

    listsort_x = sorted(coord_proc, key=lambda x: (-x[0]))
    # Dann für jeden Punkt den Rang dazuschrieben
    list_add_rowcount_to_column(listsort_x)
    # nach y sortieren und den Rang hinzufuegen
    listsort_x = sorted(listsort_x, key=lambda x: (x[1]))
    list_plus_rowcount_to_column(listsort_x, 4)

    listsort_x = sorted(listsort_x, key=lambda x: (-x[4], x[2]))
    koordinate1 = listsort_x[0]

    if koordinate2[0] != koordinate1[0] and koordinate2[1] != koordinate1[1]:
        distance = sqrt((koordinate2[0] - koordinate1[0]) ** 2 + (koordinate2[1] - koordinate1[1]) ** 2 + (koordinate2[2] - koordinate1[2]) ** 2)
    elif koordinate2[0] == koordinate1[0]:
        distance = abs(koordinate2[1] - koordinate1[1])
    elif koordinate2[1] == koordinate1[1]:
        distance = abs(koordinate2[0] - koordinate1[0])

    return distance


def calculate_distance_org(coord_proc, slope):
    # x y z (rang)

    #Ranking für jeden Punkt ermitteln
    # dazu werte nach z sortieren
    listsort = sorted(coord_proc, key=lambda x: (-x[2]))
    # Dann für jeden Punkt den Rang dazuschrieben
    list_add_rowcount_to_column(listsort)

    koordinate1 = []
    koordinate2 = []

    if slope >= 180 or slope <= -180:
        #Punkt 1 xmin und ymax \
        #dazu werte nach x sortieren

        listsort_1 = sorted(listsort, key=lambda x: (x[0]))
        listsort_1 = list_plus_rowcount_to_column(listsort_1, 3)
        #nach y sortieren (absteigend) und den Rang hinzufuegen
        listsort_1 = sorted(listsort_1, key=lambda x: (-x[1]))
        listsort_1 = list_plus_rowcount_to_column(listsort_1, 3)
        #Nach Rang sortieren
        listsort_1 = sorted(listsort_1, key=lambda x: (x[3]))
        #Erste Koordinate ist oben links

        koordinate1 = listsort_1[0]

        #Punkt2 xmax, ymin
        #Sortieren nach höchstem x
        listsort = list_column_zero(listsort, 3)

        listsort_2 = sorted(listsort, key=lambda x: (-x[2]))
        listsort_2 = list_plus_rowcount_to_column(listsort_2, 3)
        listsort_2 = sorted(listsort, key=lambda x: (-x[0]))
        # Dann für jeden Punkt den Rang dazuschrieben
        listsort_2 = list_plus_rowcount_to_column(listsort_2, 3)
        # nach y sortieren und den Rang hinzufuegen
        listsort_2 = sorted(listsort_2, key=lambda x: (x[1]))
        listsort_2 = list_plus_rowcount_to_column(listsort_2, 3)
        listsort_2 = sorted(listsort_2, key=lambda x: (x[3]))
        koordinate2 = listsort_2[0]


    elif slope > -180 and slope < 180:
        # Punkt 1 xmin und ymin /
        # dazu werte nach x sortieren

        listsort_2 = sorted(listsort, key=lambda x: (x[0]))
        listsort_2 = list_plus_rowcount_to_column(listsort_2, 3)
        # nach y sortieren (absteigend) und den Rang hinzufuegen
        listsort_2 = sorted(listsort_2, key=lambda x: (x[1]))
        listsort_2 = list_plus_rowcount_to_column(listsort_2, 3)
        # Nach Rang sortieren
        listsort_2 = sorted(listsort_2, key=lambda x: (x[3]))
        # Erste Koordinate ist oben links

        koordinate1 = listsort_2[0]

        # Punkt2 maxx, ymax
        # Sortieren nach höchstem x
        listsort = list_column_zero(listsort, 3)

        listsort_2 = sorted(listsort, key=lambda x: (-x[2]))
        listsort_2 = list_plus_rowcount_to_column(listsort_2, 3)
        listsort_2 = sorted(listsort, key=lambda x: (-x[0]))
        # Dann für jeden Punkt den Rang dazuschrieben
        listsort_2 = list_plus_rowcount_to_column(listsort_2, 3)
        # nach y sortieren und den Rang hinzufuegen
        listsort_2 = sorted(listsort_2, key=lambda x: (-x[1]))
        listsort_2 = list_plus_rowcount_to_column(listsort_2, 3)
        listsort_2 = sorted(listsort_2, key=lambda x: (x[3]))
        koordinate2 = listsort_2[0]




    if koordinate2[0] != koordinate1[0] and koordinate2[1] != koordinate1[1]:
        distance = sqrt((koordinate2[1] - koordinate1[1])**2 + (koordinate2[0] - koordinate1[0])**2 + (koordinate2[2] - koordinate1[2])**2)
    elif koordinate2[0] == koordinate1[0]:
        distance = abs(koordinate2[1] - koordinate1[1])
    elif koordinate2[1] == koordinate1[1]:
        distance = abs(koordinate2[0] - koordinate1[0])

    return distance
'''

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
        # instantiate an empty list for the transformed coordinates and other values
        # instantiate lists for the x and y values
        x_coord_proc = []
        y_coord_proc = []
        z_coord_proc = []
        selection_proc = []
        profilnr_proc =[]
        id_proc = []
        rangcheck_orginal = []
        # write the x and v values in the corresponding lists
        for i in range(len(coord_proc)):
            x_coord_proc.append(coord_proc[i][0])
            y_coord_proc.append(coord_proc[i][1])
            z_coord_proc.append(coord_proc[i][2])
            #CHANGE
            selection_proc.append(coord_proc[i][5])
            profilnr_proc.append(coord_proc[i][4])
            id_proc.append(coord_proc[i][6])
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

        #original_distance = calculate_distance_org(rangcheck_orginal, slope_deg)


        #if slope > 0 and slope < 1 and coord_proc[0][3] in ["E"]:
        #    slope_deg = 90
        #    QgsMessageLog.logMessage(str(profilnr_proc[0]), 'sonderfall')
        #if (profilnr_proc[0] == '8' or profilnr_proc[0] == '37' ):
        #    QgsMessageLog.logMessage(str(profilnr_proc[0]), 'steigung')
        #    QgsMessageLog.logMessage(str(slope), 'steigung')
        #    QgsMessageLog.logMessage(str((atan(slope) * 180) / pi), 'steigung')

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
            y_slope_deg = -slope_deg

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




































