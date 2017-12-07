# -*- coding: utf-8 -*-
from __future__ import division, print_function
import scipy
from math import atan, fabs, pi, cos, sin
from numpy import mean

from src.handlers.ErrorHandler import ErrorHandler, CoordReader
from src.data_objects.TransformationLists import TransformationLists, SlopeVarLists
from src.data_objects.Coordinates import RotatePoints


class SlopeCalculator:
    """
    Takes care of all slope related calculations
    """
    def __init__(self):
        pass

    def calculateDiffernceValues(self, x_coord_proc, y_coord_proc):
        """
        substracts the min value from the coordinats
        processed from every single coordinate value
        :param x_coord_proc: float[]
        :param y_coord_proc: float[]
        :return: SlopeVarLists
        """
        slopeVars = SlopeVarLists()
        minX = min(x_coord_proc)
        minY = min(y_coord_proc)
        i = 0
        for x_coord in x_coord_proc:
            slopeVars.x.append(x_coord - minX)
            slopeVars.y.append(y_coord_proc[i] - minY)
            i += 1

        return slopeVars

    def calculateSlope(self, slopeVals=None):
        """
        calculates the actual slope using linear regression
        :param slopeVals: SlopeVarLists
        :type slopeVals: SlopeVarLists
        :return:
        """
        return scipy.stats.linregress(scipy.array(slopeVals.x), scipy.array(slopeVals.y))[0]

    def getSlopeInDegree(self, x_coord_proc, y_coord_proc, view_name):
        """
        calculates from the given x and y coordinates the slope in degree
        :param x_coord_proc: float[]
        :param y_coord_proc: float[]
        :param view_name:
        :return: float
        """
        diffVals = self.calculateDiffernceValues(x_coord_proc, y_coord_proc)
        slope = self.calculateSlope(diffVals)
        slope_deg = 0.0
        if slope < 0 and view_name in ["N", "E"]:
            slope_deg = 180 - fabs((atan(slope) * 180) / pi) * -1
        elif slope < 0 and view_name in ["S", "W"]:
            slope_deg = fabs((atan(slope) * 180) / pi)
        elif slope > 0 and view_name in ["S", "E"]:
            slope_deg = ((atan(slope) * 180) / pi) * -1
        elif slope > 0 and view_name in ["N", "W"]:
            slope_deg = 180 - ((atan(slope) * 180) / pi)
        elif slope == 0 and view_name == "N":
            slope_deg = 180

        return slope_deg

    def changeRadToDegree(self, z_slope):
        """
        makes the conversion between radians and degree
        :param z_slope: float
        :return: float
        """
        z_slope_deg = 0.0
        if z_slope < 0:
            z_slope_deg = -(90 - fabs(((atan(z_slope) * 180) / pi)))
        elif z_slope > 0:
            z_slope_deg = 90 - ((atan(z_slope) * 180) / pi)
        elif z_slope == 0:
            z_slope_deg = 0.0

        return z_slope_deg

    def getSinSlope(self, slopeDeg):
        """
        calculates the sinus from the corner in radian
        :param slopeDeg:
        :return:
        """
        return sin(slopeDeg / 180 * pi)

    def getCosSlope(self, slopeDeg):
        """
        calculates the sinus from the corner in radian
        :param slopeDeg:
        :return:
        """
        return cos(slopeDeg / 180 * pi)


class CoordinatesTransformer:
    """
    Responsible for all the actual coordinate transformation
    """
    def __init__(self, slopeCalc):
        """

        :param slopeCalc: SlopeCalculator
        :type slopeCalc: SlopeCalculator
        """
        self.slopeCalc = slopeCalc

    def calculatePointOfRoatation(self, a_list, b_list):
        """
        calculates the rotation center
        :param a_list:
        :param b_list:
        :return: RotatePoints
        """
        return RotatePoints(mean(a_list), mean(b_list))

    def collectTransformCoordinates(self, a_list, b_list, c_list, slope_deg):
        """
        uses the given list of coordinate points and transforms them
        :param a_list:
        :param b_list:
        :param c_list:
        :param slope_deg:
        :return: TransformationLists
        """
        a_trans = []
        b_trans = []
        c_trans = []

        rotatePoints = self.calculatePointOfRoatation(a_list, b_list)

        # create a variable for the loop
        run_var = range(len(a_list))

        for idx in run_var:
            trans_dict = self.calculateTransformation(rotatePoints, a_list[idx], b_list[idx], slope_deg)
            a_trans.append(trans_dict['a'])
            b_trans.append(trans_dict['b'])
            c_trans.append(c_list[idx] + rotatePoints.b - mean(c_list))

        return TransformationLists(a_trans, b_trans, c_trans)

    def calculateTransformation(self, rotatePoints, a, b, slope_deg):
        """
        the actual transformation of the coordinates
        :param rotatePoints:
        :param a:
        :param b:
        :param slope_deg:
        :return: dictionary
        """
        diffa = (a - rotatePoints.a)
        diffb = (b - rotatePoints.b)
        sinVal = self.slopeCalc.getSinSlope(slope_deg)
        cosVal = self.slopeCalc.getCosSlope(slope_deg)
        aTrans = (rotatePoints.a + diffa * cosVal - diffb * sinVal)
        bTrans = (rotatePoints.b + diffa * sinVal + diffb * cosVal)
        return {'a': aTrans, 'b': bTrans}

    def assembleTransformedCoordList(self, trans_list, coord_proc):
        """
        adds the profile name to the translist items and returns a new list
        :param trans_list: TransformationLists
        :param coord_proc: float[]
        :return: float[]
        """
        coord_trans = []
        i = 0
        for vars in trans_list:
            vars.append(coord_proc[i].profile_name)
            coord_trans.append(vars)
            i += 1

        return coord_trans


class ProfileTransformer:
    """
    Main class of profileAAR
    """
    def __init__(self, coordReader, coordTransform, slopeCalculator, errorHandler):
        """
        constructor
        :type coordReader: CoordReader
        :param coordTransform: CoordinatesTransformer
        :type coordTransform: CoordinatesTransformer
        :type slopeCalculator: SlopeCalculator
        :type errorHandler: ErrorHandler
        """
        self.coordReader = coordReader
        self.transformator = coordTransform
        self.slopeCalculator = slopeCalculator
        self.errorHandler = errorHandler

    def transformation(self, coord_proc, method, direction):
        """
        main function
        :param coord_proc:
        :param method:
        :param direction:
        :return:
        """
        coord_trans, slope_deg, transList = self.rotateMainAxis(coord_proc)

        #self.errorHandler.result_check(coord_trans)

        if method == "surface":
            # If the aim is to get the view of the surface, the x-axis has to be rotated aswell
            coord_trans = self.transformYZAxis(coord_proc, coord_trans, transList)

        if direction == "original":
            # If the direction is in the "original" setting, the points have to be rotated
            # back to their original orientation
            coord_trans = self.transformXZAxis(coord_proc, coord_trans, transList, slope_deg)

        return coord_trans

    def rotateMainAxis(self, coord_proc):
        """
        transform the main axis
        :param coord_proc:
        :return:
        """
        x_coord_proc = self.coordReader.getListOfX(coord_proc)
        y_coord_proc = self.coordReader.getListOfY(coord_proc)
        z_coord_proc = self.coordReader.getListOfZ(coord_proc)

        slope_deg = self.slopeCalculator.getSlopeInDegree(x_coord_proc, y_coord_proc, coord_proc[0].view_name)

        transList = self.transformator.collectTransformCoordinates(x_coord_proc, y_coord_proc, z_coord_proc, slope_deg)

        # instantiate lists for the transformed coordinates
        coord_trans = self.transformator.assembleTransformedCoordList(transList, coord_proc)
        return coord_trans, slope_deg, transList

    def transformXZAxis(self, coord_proc, coord_trans, transList, slope_deg):
        """
        transforms the x and z axis
        :param coord_proc:
        :param coord_trans:
        :param transList: TransformationLists
        :param slope_deg: float
        :return: mixed[]
        """
        # the rotation angle is the negative angle of the first rotation
        y_slope_deg = -slope_deg
        rotate_points = self.transformator.calculatePointOfRoatation(transList.x_list, transList.z_list)
        # rewrite the lists for the x and z values
        transList.emptyX()
        transList.emptyZ()
        for coords in coord_trans:
            trans_dict = self.transformator.calculateTransformation(rotate_points, coords[0], coords[2],
                                                                    y_slope_deg)
            transList.x_list.append(trans_dict['a'])
            transList.z_list.append(trans_dict['b'])

        # empty and rewrite the output list
        coord_trans = self.transformator.assembleTransformedCoordList(transList, coord_proc)
        return coord_trans

    def transformYZAxis(self, coord_proc, coord_trans, transList):
        """
        transform y and z axis
        :param coord_proc:
        :param coord_trans:
        :param transList:
        :return:
        """
        z_slope_deg = self.getZSlopeDeg(transList)
        rotate_points = self.transformator.calculatePointOfRoatation(transList.y_list, transList.z_list)

        transList.emptyY()
        transList.emptyZ()

        for coords in coord_trans:
            trans_dict = self.transformator.calculateTransformation(rotate_points, coords[1], coords[2],
                                                                    z_slope_deg)
            transList.y_list.append(trans_dict['a'])
            transList.z_list.append(trans_dict['b'])

        # empty and rewrite the output list
        coord_trans = self.transformator.assembleTransformedCoordList(transList, coord_proc)
        return coord_trans

    def getZSlopeDeg(self, transList):
        """
        calculate the Z slope value in degree
        :param transList:
        :return:
        """
        slope_vars = SlopeVarLists()
        for vars in transList:
            slope_vars.x.append(vars['y'] - transList.getMinYZ())
            slope_vars.y.append(vars['z'] - transList.getMinYZ())
        z_slope = self.slopeCalculator.calculateSlope(slope_vars)
        z_slope_deg = self.slopeCalculator.changeRadToDegree(z_slope)
        return z_slope_deg
