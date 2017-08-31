# -*- coding: utf-8 -*-
"""
/***************************************************************************
 profileAAR
                                 A QGIS plugin
 profileAAR des
                             -------------------
        begin                : 2017-08-31
        copyright            : (C) 2017 by Moritz Mennenga / NIhK WHV / ISAAKiel
        email                : mennenga@nihk.de
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load profileAAR class from file profileAAR.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .profileAAR import profileAAR
    return profileAAR(iface)
