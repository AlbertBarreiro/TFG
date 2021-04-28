from PyQt5 import QtCore, QtGui
import sys
from pprint import pprint
from PyQt5.QtWidgets import  QWidget,QGridLayout,QApplication

import numpy as np
from PyQt5.QtCore import Qt, QSize, QMargins, QDir, QPoint, QPointF, QRectF, QTimer, pyqtSlot, pyqtSignal, QObject, QSettings, QFileInfo, QModelIndex
from PyQt5.QtGui import QFontDatabase, QFont, QPen, QBrush, QColor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem


class MyGText(QGraphicsTextItem):

    focusOut = pyqtSignal()

    def __init__(self, parent=None, scene=None):
        super(QGraphicsTextItem, self).__init__(parent, scene)

    def focusOutEvent(self, event):
        self.focusOut.emit()
        QGraphicsTextItem.focusOutEvent(self,event)


class Grid:

    def __init__(self):

        self.width = 0
        self.height = 0
        self.nrow = 0
        self.ncol = 0
        self.offx = 0
        self.offy = 0

        self.scene = None
        self.cell_values = None
        self.notes = []
        self.grid_rects = []


    def save(self):

        dict_to_save = {}

        dict_to_save["width"] = self.width
        dict_to_save["height"] = self.height
        dict_to_save["nrow"] = self.nrow
        dict_to_save["ncol"] = self.ncol
        dict_to_save["offx"] = self.offx
        dict_to_save["offy"] = self.offy
        dict_to_save["cell_values"] = self.cell_values.tolist()

        return dict_to_save

    def fromDict(self, dict):

        self.width = dict["width"]
        self.height = dict["height"]
        self.nrow = dict["nrow"]
        self.ncol = dict["ncol"]
        self.offx = dict["offx"]
        self.offy = dict["offy"]
        self.cell_values = np.asarray(dict["cell_values"])


    def setScene(self, scene):

        self.scene = scene

    def setGrid(self, width, height, nrow, ncol):

        self.width = width
        self.height = height
        self.nrow = nrow
        self.ncol = ncol

        # cells values
        self.cell_values = np.zeros((self.nrow, self.ncol))

        # cells dictionary notes
        self.dict_notes = {}
        positions = [(i, j) for i in range(self.nrow) for j in range(self.ncol)]
        for k in positions:
            self.dict_notes[k] = ""

    def setGridPosition(self, posx, posy):

        self.offx = posx
        self.offy = posy

        for rect in self.grid_rects:
            rect.setPos(self.offx, self.offy)

    def drawGrid(self):
        
        cell_width = self.width / self.ncol
        cell_height = self.height / self.nrow

        pen_white = QPen(Qt.white, 2, Qt.SolidLine)
        pen_white.setCosmetic(True)

        brush = QBrush(Qt.SolidPattern)
        brush.setColor(QColor(255, 255, 255, 0))

        brush25 = QBrush(Qt.DiagCrossPattern)
        brush25.setColor(QColor(255, 255, 255, 200))

        brush50 = QBrush(Qt.SolidPattern)
        brush50.setColor(QColor(255, 255, 255, 125))

        for c in range(0, self.ncol):
            for r in range(0, self.nrow):
                xc = c * cell_width
                yc = r * cell_height

                value = self.cell_values[r, c]

                if value == 0:
                    rect = self.scene.addRect(xc, yc, cell_width-1, cell_height-1, pen=pen_white, brush=brush)
                elif value == 1:
                    rect = self.scene.addRect(xc, yc, cell_width-1, cell_height-1, pen=pen_white, brush=brush25)
                elif value == 2:
                    rect = self.scene.addRect(xc, yc, cell_width-1, cell_height-1, pen=pen_white, brush=brush50)

                rect.setPos(self.offx, self.offy)
                self.grid_rects.append(rect)

        for note in self.notes:
            self.scene.addItem(note)

    def setVisible(self, visible=True):
        for rect in self.grid_rects:
            rect.setVisible(visible)

    def undrawGrid(self):
        for rect in self.grid_rects:
            self.scene.removeItem(rect)
        del self.grid_rects[:]

        for note in self.notes:
            self.scene.removeItem(note)

    def setOpacity(self, opacity):

        for rect in self.grid_rects:
            rect.setOpacity(opacity)

    def changeCellState(self, x, y, state):
        """
        Assign the cell indexed by the x,y coordinates the given state.
        If state is None the cell cycles between the different states.
        """
        cell_width = self.width / self.ncol
        cell_height = self.height / self.nrow

        c = int((x - self.offx)/ cell_width)
        r = int((y - self.offy) / cell_height)

        if state is None:
            self.cell_values[r, c] = (self.cell_values[r, c] + 1) % 3
        else:
            self.cell_values[r, c] = state

        self.undrawGrid()
        self.drawGrid()

    def addNote(self, x, y, txt):

        font = QFont("Robota", 15)
        text_item = MyGText()
        text_item.setPlainText(txt)
        text_item.setFont(font)
        text_item.setDefaultTextColor(Qt.white)
        text_item.setPos(x, y)
        text_item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable)
        text_item.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextEditable)
        self.notes.append(text_item)
        self.scene.addItem(text_item)
       # text_item.focusOut.connect(self.isEmpty)

    @pyqtSlot()
    def isEmpty(self):
        # text_item = self.sender

         pass





