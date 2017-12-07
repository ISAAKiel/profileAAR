from qgis.core import *
from numpy import std, mean
import sys
from math import pi, fabs
import matplotlib.pyplot as plt
import scipy

from ..gis_api.MessageWrapper import MessageWrappper
from ..gis_api.Logger import Logger
from ..data_objects.Coordinates import Coordinates

class CoordReader:
    def getListOfX(self, coordList):
        list = []
        for coor in coordList:
            list.append(coor.point.getXVal())

        return list

    def getListOfY(self, coordList):
        list = []
        for coor in coordList:
            list.append(coor.point.getYVal())

        return list

    def getListOfZ(self, coordList):
        list = []
        for coor in coordList:
            list.append(coor.point.getZVal())

        return list


class ErrorHandler:
    def __init__(self, messageWrapper, logger, coordReader):
        """
        :param messageWrapper used to communicate with qgis classe for seperation
        :type messageWrapper: MessageWrappper
        :param logger Logger
        :type logger Logger
        :param coordReader Helper Class provides access to
            the coordinate Object inside the coordList
        :type coordReader CoordReader
        """
        self.messageOutput = messageWrapper
        self.logger = logger
        self.coordReader = coordReader

    def checkViews(self, views, profile_name):
        self._checkViewValue(profile_name, views)

        self._checkViewDirection(profile_name, views)

    # Checks that have to do on every single Profile
    def checkCoords(self, coord_proc, profile_name):
        # TODO: check for consistency before calculation
        # TODO: check for spatial consistency (no points should be more than x meters apart)

        self._checkProfileLength(coord_proc, profile_name, min_length=4)


        # check if the coordinates x, y, z fall into 2 sigma range
        # instance a table like list of lists with i rows and j columns
        self._checkCoordinateDeviation(coord_proc, profile_name, devRange=2)

    def _checkCoordinateDeviation(self, coord_proc, profile_name, devRange):
        listX = self.coordReader.getListOfX(coord_proc)
        listY = self.coordReader.getListOfY(coord_proc)
        listZ = self.coordReader.getListOfZ(coord_proc)
        self._checkDeviation(listX, profile_name, 'x',  devRange)
        self._checkDeviation(listY, profile_name, 'y', devRange)
        self._checkDeviation(listZ, profile_name, 'z', devRange)

    def _checkViewDirection(self, profile_name, view_check, allowed_directions = ["N", "E", "S", "W"]):
        """
        check if the view is one of the given allowed direction, by default the cardinal directions
        :param profile_name:
        :param view_check:
        :param allowed_directions:
        :return:
        """
        if view_check[0].upper() not in allowed_directions:
            self._triggerError("The view value is not one of the four cardinal directions. Error on profile: " + str(
                profile_name))

    def _checkViewValue(self, profile_name, view_check):
        """
        check if the view value is the same in all features
        :param profile_name:
        :param view_check:
        :return:
        """
        if len(view_check) != 1:
            self._triggerError(
                "The view column of your data is inconsistant (either non or two different views are present). Error on profile: " + str(
                    profile_name))

    def _checkProfileLength(self, coord_proc, profile_name, min_length):
        """
        Checks if the given profile length is lower then the given min_lengt and raises an error if so
        :param coord_proc:
        :param profile_name:
        :param min_length:
        :return:
        """
        if len(coord_proc) < min_length:
            self._triggerError("A profile needs min. " + str(min_length) + " points. Error on profile: " + str(
            profile_name))

    def _triggerError(self, message):
        self.messageOutput.printError(message)
        # cancel execution of the script
        sys.exitfunc()

    def field_check(self, layer, z_field):
        # Check if the vectorlayer is projected
        if layer.crs().geographicFlag() == True:
            self.messageOutput.printInformation("Layer " + layer.name() + " is not projected. Please choose an projected reference system.")
            # cancel execution of the script
            sys.exitfunc()

        # check the z-field
        for field in layer.fields():
            # Take a look for the z Field
            if str(field.name()) == str(z_field):
                # if the z value is not a float
                if field.typeName() != "Real" and field.typeName() != "double":
                    # Give a message
                    self.messageOutput.printError("The z-Value needs to be a float. Check the field type of the z-Value")
                    # cancel execution of the script
                    sys.exitfunc()



                    # checks if the inputfields are filled correct

    def input_check(self, value):
        if str(value) == "":
            self.messageOutput.printError("Please choose an output file!")
            # cancel execution of the script
            sys.exitfunc()

    def result_check(self, coord_trans):
        # for checking the accuracy of the points we create an line throught the profile. (Do it the easy way: y-value of a point - mean y-Value)
        # the distances from each point to the profile will lead to a comparable number
        # mean value of all Y values
        ymean = mean(self.coordReader.getListOfY(coord_trans))
        # list for the result
        check_result = []
        # go throught the profile
        for coord in coord_trans:
            # calculate for each point the absolute distance to a virtual line that is parallel to the x axis in the middle of the profile
            check_result.append(fabs(coord.point.getYVal() - ymean))
        # print the min max and mean values
        self.logger.log('Profile:' + str(coord_trans[0].view_name))
        self.logger.log('Y-Error min:' + str(round(min(check_result), 2)))
        self.logger.log('Y-Error mean:' + str(round(mean(check_result), 2)))
        self.logger.log('Y-Error max:' + str(round(max(check_result), 2)))
        self.logger.log(' ')

    def _checkDeviation(self, coordList, profile_name, currentLetter,  devRange):
        xyz_lower = mean(coordList) - (devRange * std(coordList))
        xyz_upper = mean(coordList) + (devRange * std(coordList))
        i = 0
        for val in coordList:
            if val < xyz_lower or val > xyz_upper:
                self.logger.log(
                    'Range profile ' + str(profile_name) + ': ' + str(xyz_lower) + " - " + str(xyz_upper))
                self.logger.log('value ' + str(val))
                self.messageOutput.printWarning(
                    "Warning: Profile " + str(profile_name) + ': ' + currentLetter + 'Pt ' + str(
                        i + 1) + ' exceeds the 2std interval of ' + currentLetter)
            i += 0

    def checkLayer(self, layer):
        if not layer:
            self.messageOutput.printError("Failed to open " + self.dlg.outputPath.text() + ".")