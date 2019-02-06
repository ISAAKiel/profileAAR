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


def criticalMessageToBar (self, header, text):
    self.qgisInterface.messageBar().pushMessage(header, text, level=QgsMessageBar.CRITICAL)

def warningMessageToBar (self, header, text):
    self.qgisInterface.messageBar().pushMessage(header, text)

def exportError (self):
    print "Error when creating shapefile: "
    criticalMessageToBar(self, 'Export Error', 'Error when creating shapefile')

def printLogMessage(self,message,tab):
    QgsMessageLog.logMessage(message, tab)
