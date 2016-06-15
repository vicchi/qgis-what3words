# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
from qgis.core import *
from qgis.gui import *
from qgis.utils import iface
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from w3w import what3words
from apikey import apikey

class W3WMapTool(QgsMapTool):

    epsg4326 = QgsCoordinateReferenceSystem("EPSG:4326")

    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.setCursor(Qt.CrossCursor)
        print apikey()
        self.w3w = what3words(apikey=apikey())

    def toW3W(self, pt):
        canvas = iface.mapCanvas()
        canvasCrs = canvas.mapSettings().destinationCrs()
        transform = QgsCoordinateTransform(canvasCrs, self.epsg4326)
        pt4326 = transform.transform(pt.x(), pt.y())
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            w3wCoords = self.w3w.reverseGeocode(pt4326.y(), pt4326.x())["words"]
        except Exception,e :
            w3wCoords = None
        finally:
            QApplication.restoreOverrideCursor()

        return w3wCoords

    def canvasReleaseEvent(self, e):
        pt = self.toMapCoordinates(e.pos())
        w3wCoord = self.toW3W(pt)
        if w3wCoord:
            iface.messageBar().pushMessage("what3words", "The 3 word address: '{}' has been copied to the clipboard".format(w3wCoord), level=QgsMessageBar.INFO, duration=6)
            clipboard = QApplication.clipboard()
            clipboard.setText(w3wCoord)
        else:
            iface.messageBar().pushMessage("what3words", "Could not convert the selected point to a 3 word address", level=QgsMessageBar.WARNING, duration=3)
