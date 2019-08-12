# TagLab                                               
# A semi-automatic segmentation tool                                    
#
# Copyright(C) 2019                                         
# Visual Computing Lab                                           
# ISTI - Italian National Research Council                              
# All rights reserved.                                                      
                                                                          
# This program is free software; you can redistribute it and/or modify      
# it under the terms of the GNU General Public License as published by      
# the Free Software Foundation; either version 2 of the License, or         
# (at your option) any later version.                                       
                                                                           
# This program is distributed in the hope that it will be useful,           
# but WITHOUT ANY WARRANTY; without even the implied warranty of            
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             
#GNU General Public License (http://www.gnu.org/licenses/gpl.txt)          
# for more details.                                               

""" PyQt image viewer widget for a QPixmap in a QGraphicsView scene with mouse zooming and panning.
    The viewer has also drawing capabilities.
"""

import os.path
from PyQt5.QtCore import Qt, QPointF, QRectF, pyqtSignal, QT_VERSION_STR
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPainterPath
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QFileDialog


class QtImageViewerPlus(QGraphicsView):
    """ PyQt image viewer widget with annotation capabilities.
    QGraphicsView handles a scene composed by an image plus shapes (rectangles, polygons, blobs).
    The input image (it must be a QImage) is internally converted into a QPixmap.

    WORKING MODE:

      - NORMAL              -> image viewer with pan and zoom capabilities
      - RECTS_ANNOTATION    -> annotate use a rectangle
      - POLYGONS_ANNOTATION -> annotate use a polygon
      - BLOBS_ANNOTATION    -> add or remove a blob

    KEYBOARDS:

      - SPACEBAR        : toggle between different working modes

    MOUSE INTERACTION:

      - NORMAL MODE:

          Left mouse button drag: pan image.
          Mouse wheel: zoom in/zoom out.

      - RECTS_ANNOTATION MODE:

          - Left mouse button drag: define the rectangle.

      - BLOBS_ANNOTATION MODE:

          Left mouse button: select a blob
          Right mouse button: remove a selected blob

      - POLYGONS_ANNOTATION MODE:

          Left mouse button: add a point.
          Right mouse button: remove a point.
          Left mouse button doubleclick: close the polygon.

    """

    # Mouse button signals emit image scene (x, y) coordinates.
    leftMouseButtonPressed = pyqtSignal(float, float)
    rightMouseButtonPressed = pyqtSignal(float, float)
    leftMouseButtonReleased = pyqtSignal(float, float)
    rightMouseButtonReleased = pyqtSignal(float, float)
    leftMouseButtonDoubleClicked = pyqtSignal(float, float)
    rightMouseButtonDoubleClicked = pyqtSignal(float, float)
    mouseMoveLeftPressed = pyqtSignal(float, float)

    # custom signal
    viewUpdated = pyqtSignal()

    def __init__(self):
        QGraphicsView.__init__(self)

        self.setStyleSheet("background-color: rgb(40,40,40)")

        self.mode_list = ["NORMAL", "RECTS_ANNOTATION", "BLOBS_ANNOTATION", "POLYGONS_ANNOTATION"]
        self.current_mode = 0
        self.mode = self.mode_list[self.current_mode]

        # Image is displayed as a QPixmap in a QGraphicsScene attached to this QGraphicsView.
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # Store a local handle to the scene's current image pixmap.
        self._pxmapitem = None

        # current image size
        self.imgwidth = 0
        self.imgheight = 0

        # Image aspect ratio mode.
        self.aspectRatioMode = Qt.KeepAspectRatio

        # Set scrollbar
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.verticalScrollBar().valueChanged.connect(self.viewUpdated)
        self.horizontalScrollBar().valueChanged.connect(self.viewUpdated)



        # Panning is enabled if and only if the image is greater than the viewport.
        self.panEnabled = True
        self.zoomEnabled = True

        self.clicked_x = 0
        self.clicked_y = 0

        # zoom is always active
        self.zoom_factor = 1.0
        self.ZOOM_FACTOR_MIN = 0.02
        self.ZOOM_FACTOR_MAX = 10.0

        # transparency
        self.opacity = 1.0

        MIN_SIZE = 250
        self.pixmap = QPixmap(MIN_SIZE, MIN_SIZE)
        self.overlay_image = QImage(1, 1, QImage.Format_ARGB32)

        self.viewport().setMinimumWidth(MIN_SIZE)
        self.viewport().setMinimumHeight(MIN_SIZE)

        self.resetTransform()
        self.setMouseTracking(True)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        self.setContextMenuPolicy(Qt.CustomContextMenu)


    def disableScrollBars(self):

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def hasImage(self):
        """ Returns whether or not the scene contains an image pixmap.
        """
        return self._pxmapitem is not None

    def image(self):
        """ Returns the scene's current image as a QImage.
        """
        if self.hasImage():
            return self._pxmapitem.pixmap().toImage()
        return None

    def enablePan(self):
        self.panEnabled = True

    def disablePan(self):
        self.panEnabled = False

    def enableZoom(self):
        self.zoomEnabled = True

    def disableZoom(self):
        self.zoomEnabled = False

    def setImage(self, image, zoomf=0.0):
        """
        Set the scene's current image (input image must be a QImage)
        For calculating the zoom factor automatically set it to 0.0.
        """
        if type(image) is QImage:
            imageARGB32 = image.convertToFormat(QImage.Format_ARGB32)
            self.pixmap = QPixmap.fromImage(imageARGB32)
            self.imgwidth = image.width()
            self.imgheight = image.height()
        else:
            raise RuntimeError("Argument must be a QImage.")

        if self.hasImage():
            self._pxmapitem.setPixmap(self.pixmap)
        else:
            self._pxmapitem = self.scene.addPixmap(self.pixmap)

        # Set scene size to image size (!)
        self.setSceneRect(QRectF(self.pixmap.rect()))

        # calculate zoom factor
        pixels_of_border = 10
        zf1 = (self.viewport().width() - pixels_of_border) / self.imgwidth
        zf2 = (self.viewport().height() - pixels_of_border) / self.imgheight

        zf = min(zf1, zf2)
        self.zoom_factor = zf

        self.updateViewer()

    def updateImage(self, image):

        if type(image) is QImage:
            imageARGB32 = image.convertToFormat(QImage.Format_ARGB32)
            self.pixmap = QPixmap.fromImage(imageARGB32)
            self.imgwidth = image.width()
            self.imgheight = image.height()
        else:
            raise RuntimeError("Argument must be a QImage.")

        self._pxmapitem.setPixmap(self.pixmap)

        # if an overlay exists it must be drawn
        if self.overlay_image.width() > 1:
            self.drawOverlayImage()

        self.updateViewer()

    def setOpacity(self, opacity):
        self.opacity = opacity

    def loadImageFromFile(self, fileName=""):
        """ Load an image from file.
        """
        image = QImage(fileName)
        self.setImage(image)

    def setOverlayImage(self, image):
        self.overlay_image = image.convertToFormat(QImage.Format_ARGB32)
        self.drawOverlayImage()

    def drawOverlayImage(self):

        if self.overlay_image.width() > 1:
            pxmap = self.pixmap.copy()
            p = QPainter()
            p.begin(pxmap)
            p.setOpacity(self.opacity)
            p.drawImage(0, 0, self.overlay_image)
            p.end()

            self._pxmapitem.setPixmap(pxmap)

    def setWorkingMode(self, mode):
        """
        Set the current working mode of the viewer.
        'mode' should be an integer with the following values:

          mode = 0 -> NORMAL
          mode = 1 -> ANNOTATION WITH RECTS
          mode = 2 -> ANNOTATION WITH BLOBS
          mode = 3 -> ANNOTATION WITH POLYGONS
        """
        self.mode = self.mode_list[mode]

    def updateViewer(self):
        """ Show current zoom (if showing entire image, apply current aspect ratio mode).
        """
        if not self.hasImage():
            return

        self.resetTransform()
        self.scale(self.zoom_factor, self.zoom_factor)

        painter = QPainter(self)
        self.scene.render(painter)

        # notify that the view has been updated
        #self.viewUpdated.emit()

    def setViewParameters(self, posx, posy, zoomfactor):
        self.horizontalScrollBar().setValue(posx)
        self.verticalScrollBar().setValue(posy)
        self.zoom_factor = zoomfactor
        self.updateViewer()

    def clipScenePos(self, scenePosition):
        posx = scenePosition.x()
        posy = scenePosition.y()
        if posx < 0:
            posx = 0
        if posy < 0:
            posy = 0
        if posx > self.imgwidth:
            posx = self.imgwidth
        if posy > self.imgheight:
            posy = self.imgheight

        return [posx, posy]

    def resizeEvent(self, event):
        """ Maintain current zoom on resize.
        """
        self.updateViewer()

    def mousePressEvent(self, event):
        """ Start mouse pan or zoom mode.
        """
        scenePos = self.mapToScene(event.pos())

        if event.button() == Qt.LeftButton:
            # if self.panEnabled:
            if self.panEnabled or (not self.panEnabled and event.modifiers() & Qt.ControlModifier):
                self.setDragMode(QGraphicsView.ScrollHandDrag)
            clippedCoords = self.clipScenePos(scenePos)
            self.leftMouseButtonPressed.emit(clippedCoords[0], clippedCoords[1])

        # PANNING IS ALWAYS POSSIBLE WITH WHEEL BUTTON PRESSED (!)
        # if event.button() == Qt.MiddleButton:
        #     self.setDragMode(QGraphicsView.ScrollHandDrag)

        if event.button() == Qt.RightButton:
            clippedCoords = self.clipScenePos(scenePos)
            self.rightMouseButtonPressed.emit(clippedCoords[0], clippedCoords[1])

        self.clicked_x = event.pos().x()
        self.clicked_y = event.pos().y()

        QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        """ Stop mouse pan or zoom mode (apply zoom if valid).
        """
        QGraphicsView.mouseReleaseEvent(self, event)

        scenePos = self.mapToScene(event.pos())

        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)
            clippedCoords = self.clipScenePos(scenePos)
            self.leftMouseButtonReleased.emit(clippedCoords[0], clippedCoords[1])


    def mouseMoveEvent(self, event):

        QGraphicsView.mouseMoveEvent(self, event)

        scenePos = self.mapToScene(event.pos())

        if event.buttons() == Qt.LeftButton:
            clippedCoords = self.clipScenePos(scenePos)
            self.mouseMoveLeftPressed.emit(clippedCoords[0], clippedCoords[1])

    def mouseDoubleClickEvent(self, event):

        scenePos = self.mapToScene(event.pos())

        if event.button() == Qt.LeftButton:
            self.leftMouseButtonDoubleClicked.emit(scenePos.x(), scenePos.y())

        # QGraphicsView.mouseDoubleClickEvent(self, event)

    def wheelEvent(self, event):
        """ Zoom in/zoom out.
        """

        if self.zoomEnabled:

            pt = event.angleDelta()

            self.zoom_factor = self.zoom_factor + pt.y() / 2400.0
            if self.zoom_factor < self.ZOOM_FACTOR_MIN:
                self.zoom_factor = self.ZOOM_FACTOR_MIN
            if self.zoom_factor > self.ZOOM_FACTOR_MAX:
                self.zoom_factor = self.ZOOM_FACTOR_MAX

            self.updateViewer()


        # PAY ATTENTION; THE WHEEL INTERACT ALSO WITH THE SCROLL BAR (!!)
        #QGraphicsView.wheelEvent(self, event)


