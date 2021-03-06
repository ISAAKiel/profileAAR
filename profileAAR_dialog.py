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



import os

from .resources import *

from qgis.PyQt import uic
from PyQt5.QtWidgets import QAction, QDialog, QFormLayout
import PyQt5.QtGui as QtGui



FORM_CLASS, _ = uic.loadUiType(os.path.join(

    os.path.dirname(__file__), 'profileAAR_dialog_base.ui'))





class profileAARDialog(QDialog, FORM_CLASS):

    def __init__(self, parent=None):

        """Constructor."""

        super(profileAARDialog, self).__init__(parent)

        # Set up the user interface from Designer.

        # After setupUI you can access any designer object by doing

        # self.<objectname>, and you can use autoconnect slots - see

        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html

        # #widgets-and-dialogs-with-auto-connect

        self.setupUi(self)
        
        self.icon.setPixmap(QtGui.QPixmap(':/profileAAR/img/icon.png'))

