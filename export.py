# -*- coding: utf-8 -*-
"""
/***************************************************************************
 profileAARDialog
                                 A QGIS plugin
 profileAAR des
                             -------------------
        begin                : 2017-08-31
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Moritz Mennenga / Kay Schmuetz
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
            # CHANGE
            export_fields = QgsFields()
            export_fields.append(QgsField("x", QVariant.Double))
            export_fields.append(QgsField("y", QVariant.Double))
            export_fields.append(QgsField("z", QVariant.Double))
            export_fields.append(QgsField("prnumber", QVariant.String))
            export_fields.append(QgsField("org_z", QVariant.String))
            export_fields.append(QgsField("distance", QVariant.String))
            export_fields.append(QgsField("was_used", QVariant.String))

            writer = QgsVectorFileWriter(filename, "utf-8", export_fields, QGis.WKBPoint, corrdinate_system, "ESRI Shapefile")
            if writer.hasError() != QgsVectorFileWriter.NoError:
                print "Error when creating shapefile: "

            #CHANGE
            export_feature = QgsFeature()
            for x in range(len(coord_trans)):
                for i in range(len(coord_trans[x])):
                    export_feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(coord_trans[x][i][0], coord_trans[x][i][2])))
                    #TODO Werte runden auf drei nachkommastellen
                    export_feature.setAttributes([float(coord_trans[x][i][0]), float(coord_trans[x][i][1]), float(coord_trans[x][i][2]), str(coord_trans[x][i][3]), str(coord_trans[x][i][4]), str(coord_trans[x][i][5]) , str(coord_trans[x][i][6])])
                    writer.addFeature(export_feature)



            del writer


    def export_height(self, coord_trans, filename, corrdinate_system):
            '''Create Vector Layer'''
            # CHANGE
            export_fields = QgsFields()
            export_fields.append(QgsField("prnumber", QVariant.String))
            export_fields.append(QgsField("org_z", QVariant.String))
            filename = filename.split(".shp")[0]
            filename = filename + "_height.shp"

            writer = QgsVectorFileWriter(filename, "utf-8", export_fields, QGis.WKBPoint, corrdinate_system, "ESRI Shapefile")
            if writer.hasError() != QgsVectorFileWriter.NoError:
                print "Error when creating shapefile: "
            #CHANGE
            export_feature = QgsFeature()
            for x in range(len(coord_trans)):
                # QgsMessageLog.logMessage(str(coord_trans[x]), 'MyPlugin')
                export_feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(coord_trans[x][0], coord_trans[x][2])))
                #TODO Werte runden auf drei nachkommastellen
                export_feature.setAttributes([str(coord_trans[x][3]), str(coord_trans[x][4])])
                writer.addFeature(export_feature)

            del writer


    def export_outer_profile_points_original(self, coords, filename, coordinate_system):

        export_fields = QgsFields()
        export_fields.append(QgsField("org_z", QVariant.String))
        filename = filename.split(".shp")[0]
        filename = filename + "_outer_profile_points_org.shp"

        writer = QgsVectorFileWriter(filename, "utf-8", export_fields, QGis.WKBPoint, coordinate_system,
                                     "ESRI Shapefile")
        if writer.hasError() != QgsVectorFileWriter.NoError:
            print "Error when creating shapefile: "
        # CHANGE
        export_feature = QgsFeature()
        for x in range(len(coords)):
            for i in range(len(coords[x])):
                export_feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(coords[x][i][0], coords[x][i][1])))
                # TODO Werte runden auf drei nachkommastellen
                export_feature.setAttributes([str(coords[x][i][3])])
                writer.addFeature(export_feature)
        del writer

    def export_outer_profile_points_proc(self, coords, filename, coordinate_system):

        export_fields = QgsFields()
        export_fields.append(QgsField("org_z", QVariant.String))
        filename = filename.split(".shp")[0]
        filename = filename + "_outer_profile_points_proc.shp"

        writer = QgsVectorFileWriter(filename, "utf-8", export_fields, QGis.WKBPoint, coordinate_system,
                                     "ESRI Shapefile")
        if writer.hasError() != QgsVectorFileWriter.NoError:
            print "Error when creating shapefile: "
        # CHANGE
        export_feature = QgsFeature()
        for x in range(len(coords)):
            for i in range(len(coords[x])):
                export_feature.setGeometry(QgsGeometry.fromPoint(QgsPoint(coords[x][i][0], coords[x][i][2])))
                # TODO Werte runden auf drei nachkommastellen
                export_feature.setAttributes([str(coords[x][i][3])])
                writer.addFeature(export_feature)
        del writer





