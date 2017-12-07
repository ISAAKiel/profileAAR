# -*- coding: utf-8 -*-
"""
/***************************************************************************
 profileAARDialog
                                 A QGIS plugin
 profileAAR des
                             -------------------
        begin                : 2017-08-31
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Moritz Mennenga / Kay Schmütz
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
from PyQt4.QtCore import QVariant
from qgis.core import *
class Export: 
    def __init__(self, qgisInterface):
        self.qgisInterface = qgisInterface
        
    def export(self, coord_trans, filename, corrdinate_system):
            '''Create Vector Layer'''
            
            export_fields = QgsFields()
            export_fields.append(QgsField("x", QVariant.Double))
            export_fields.append(QgsField("y", QVariant.Double))
            export_fields.append(QgsField("z", QVariant.Double))
            export_fields.append(QgsField("prnumber", QVariant.String))

            writer = QgsVectorFileWriter(filename, "utf-8", export_fields, QGis.WKBPoint, corrdinate_system, "ESRI Shapefile")
            if writer.hasError() != QgsVectorFileWriter.NoError:
                print "Error when creating shapefile: "

            export_feature = QgsFeature()
            for x in range(len(coord_trans)):
                for i in range(len(coord_trans[x])):
                    export_feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(coord_trans[x][i][0], coord_trans[x][i][2])))
                    export_feature.setAttributes([float(coord_trans[x][i][0]), float(coord_trans[x][i][1]), float(coord_trans[x][i][2]),str(coord_trans[x][i][3])])
                    writer.addFeature(export_feature)



            del writer
          