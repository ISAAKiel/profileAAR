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

from __future__ import print_function

from qgis.gui import QgsMessageBar

from qgis.core import *


def criticalMessageToBar (self, header, text):
    """
    show a critical message

    :param header: header of the message
    :type header: str, QString

    :param text: main text of the message
    :type text: str, QString
    """

    self.qgisInterface.messageBar().pushMessage(header, text, level=Qgis.Critical)


def warningMessageToBar (self, header, text):
    """
    show a warning message

    :param header: header of the message
    :type header: str, QString

    :param text: main text of the message
    :type text: str, QString
    """

    self.qgisInterface.messageBar().pushMessage(header, tex, level=Qgis.Info)


def exportError (self):
    """
    Print a message while an error occurs during exporting shape files
    """

    print("Error when creating shapefile: ")

    criticalMessageToBar(self, 'Export Error', 'Error when creating shapefile')


def printLogMessage(self,message,tab):
    """
    Print a log message

    :param message: the message to be printed
    :type tab: str, QString

    :param tab: the tab of the qgis log window
    :type message: str, QString

    """


    QgsMessageLog.logMessage(message, tab)
