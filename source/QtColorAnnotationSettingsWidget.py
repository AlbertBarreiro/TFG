import os
import json
import bisect

from PyQt5.QtCore import Qt, QSize, pyqtSlot, pyqtSignal, QEvent
from PyQt5.QtGui import QImage, QImageReader, QPixmap, QIcon, qRgb, qRed, qGreen, qBlue
from PyQt5.QtWidgets import QWidget, QScrollArea, QMessageBox, QFileDialog, QComboBox, QSizePolicy, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QSpacerItem
from source.QtSettingsWidget import QtSettingsWidget

from source.Label import Label

class QtColorAnnotationSettingsWidget(QWidget):

    create = pyqtSignal(list)
    def __init__(self, parent=None):
        super(QtColorAnnotationSettingsWidget, self).__init__(parent)


        self.labelsL = []
        self.label_colorL = []
        self.label_nameL  = []

        self.labelsR = []
        self.label_colorR = []
        self.label_nameR  = []

        self.selectedL = None
        self.selectedR = None

        self.setStyleSheet("background-color: rgb(40,40,40); color: white")
        self.setFixedSize(510, 530)

        
        top = QHBoxLayout()

        self.label = QLabel("    Add the labels you want for the annotation")
        self.label.setStyleSheet("font: 12pt")
        self.label.setAlignment(Qt.AlignCenter)
        top.addWidget(self.label)

        self.labels_layoutL = QVBoxLayout()
        self.labels_widgetL = QWidget()

        self.labels_layoutR = QVBoxLayout()
        self.labels_widgetR = QWidget()

        self.labels_widgetL.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.labels_widgetR.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        self.labels_widgetL.setLayout(self.labels_layoutL)
        self.labels_widgetL.setMinimumWidth(220)
        self.labels_widgetL.setMinimumHeight(400)
        self.labels_widgetR.setLayout(self.labels_layoutR)
        self.labels_widgetR.setMinimumWidth(220)
        self.labels_widgetR.setMinimumHeight(400)

        self.scrollL = QScrollArea()
        self.scrollL.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.scrollL.setStyleSheet("background-color: rgb(55,55,55); border: 1px solid rgb(90,90,90)")
        self.scrollL.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollL.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollL.setMaximumHeight(400)
        self.scrollL.setWidget(self.labels_widgetL)

        verticalSpacer1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.btn_add = QPushButton("Add >>")
        self.btn_add.clicked.connect(self.addLabel)

        self.btn_remove = QPushButton("<< Remove")
        self.btn_remove.clicked.connect(self.removeLabel)

        verticalSpacer2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)


        self.layoutButtons = QVBoxLayout()
        self.layoutButtons.addItem(verticalSpacer1)
        self.layoutButtons.addWidget(self.btn_add)
        self.layoutButtons.addWidget(self.btn_remove)
        self.layoutButtons.addItem(verticalSpacer2)

        self.scrollR = QScrollArea()
        self.scrollR.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.scrollR.setStyleSheet("background-color: rgb(55,55,55); border: 1px solid rgb(90,90,90)")
        self.scrollR.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollR.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollR.setMaximumHeight(400)
        self.scrollR.setWidget(self.labels_widgetR)

        mid = QHBoxLayout()
        mid.addWidget(self.scrollL)
        mid.addLayout(self.layoutButtons)
        mid.addWidget(self.scrollR)


        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.btn_create = QPushButton("Create")
        self.btn_create.clicked.connect(self.createAnnotation)

        bottom = QHBoxLayout()
        bottom.addItem(horizontalSpacer)
        bottom.addWidget(self.btn_create)


        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addLayout(mid)
        layout.addLayout(bottom)
        self.setLayout(layout)
        
        self.setWindowTitle("Creation of color annotation")
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint | Qt.WindowTitleHint)


        settings_widget = QtSettingsWidget( os.getcwd())
        default_dict_Annotatio = settings_widget.settings.value("default-dictionary",
                                                defaultValue="dictionaries/default_dictionary__color_Annotation.json", type=str)
        
        self.loadDictionary(default_dict_Annotatio)

        self.createAllLabels(True)

    def loadDictionary(self, filename):

        f = open(filename)
        dictionary = json.load(f)
        f.close()

        self.dictionary_name = dictionary['Name']
        self.dictionary_description = dictionary['Description']
        labels = dictionary['Labels']

        self.labelsL = []
        for label in labels:
            id = label['id']
            name = label['name']
            fill = label['fill']
            border = label['border']
            description = label['description']
            bisect.insort_left(self.labelsL, Label(id=id, name=name, fill=fill, border=border))


    def createAllLabels(self, isLeft):
        scroll = None
        labels_layout = None
        labels = None
        label_name = None
        label_color = None
        

        if isLeft:
            self.labels_layoutL = QVBoxLayout()
            self.label_nameL = []
            self.label_colorL = []

            scroll = self.scrollL
            labels_layout = self.labels_layoutL
            labels = self.labelsL
            label_name = self.label_nameL
            label_color = self.label_colorL
            
        else:
            self.labels_layoutR = QVBoxLayout()
            self.label_nameR = []
            self.label_colorR = []

            scroll = self.scrollR
            labels_layout = self.labels_layoutR
            labels = self.labelsR
            label_name = self.label_nameR
            label_color = self.label_colorR


        for label in labels:
            COLOR_SIZE = 20
            text = "QPushButton:flat {background-color: rgb(" + str(label.fill[0]) + "," + str(
                label.fill[1]) + "," + str(label.fill[2]) + "); border: none ;}"
            btn_color = QPushButton()
            btn_color.setFlat(True)
            btn_color.setStyleSheet(text)
            btn_color.setAutoFillBackground(True)
            btn_color.setFixedWidth(COLOR_SIZE)
            btn_color.setFixedHeight(COLOR_SIZE)
            label_color.append(btn_color)

            lbl_name = QLabel(label.name)
            lbl_name.setStyleSheet("border: none; color: lightgray;")
            lbl_name.setFixedHeight(20)
            lbl_name.installEventFilter(self)
            label_name.append(lbl_name)

            label_layout = QHBoxLayout()
            label_layout.addWidget(btn_color)
            label_layout.addWidget(lbl_name)

            labels_layout.addLayout(label_layout)

        # update the scroll area
        tempWidget = QWidget()
        tempWidget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        tempWidget.setMinimumWidth(220)
        tempWidget.setMinimumHeight(400)
        tempWidget.setLayout(labels_layout)
        scroll.setWidget(tempWidget)
       
    def eventFilter(self, object, event):

        if type(object) == QLabel and event.type() == QEvent.MouseButtonPress:

            self.highlightSelectedLabel(object)
            return False
        elif type(object) == QLabel and event.type() == QEvent.MouseButtonDblClick:

            self.moveLabel(object)
            return False

        return False

    def highlightSelectedLabel(self, lbl_clicked):

        # reset the text of all the labels
        for lbl in self.label_nameL:
            lbl.setStyleSheet("border: none; color: lightgray;")
        for lbl in self.label_nameR:
            lbl.setStyleSheet("border: none; color: lightgray;")

        # highlight the selected label
        #txt = lbl_clicked.text()
        lbl_clicked.setStyleSheet("border: 1 px; font-weight: bold; color: white;")

        if any(lbl_clicked.text() == label.name for label in self.labelsL):
            self.selectedL = lbl_clicked
            self.selectedR = None
        elif any(lbl_clicked.text() == label.name for label in self.labelsR):
            self.selectedR = lbl_clicked
            self.selectedL = None

    def moveLabel(self, lbl_clicked):
        isLeft = True

        if any(lbl_clicked.text() == label.name for label in self.labelsL):
            self.selectedL = lbl_clicked
            self.selectedR = None

        elif any(lbl_clicked.text() == label.name for label in self.labelsR):
            self.selectedR = lbl_clicked
            self.selectedL = None
            isLeft = False
        
        if isLeft:
            self.addLabel()
        else:
            self.removeLabel()


    def addLabel(self):
        if self.selectedL is not None:
            index = self.label_nameL.index(self.selectedL)
            move_label = self.labelsL[index]
            move_label_name = self.label_nameL[index]
            move_label_color = self.label_colorL[index]

            move_label_name.setStyleSheet("border: none; color: lightgray;")

            self.addLabelScrollR(move_label, move_label_name, move_label_color)

            self.labelsL.pop(index)
            self.createAllLabels(True)
    
    def removeLabel(self):
        if self.selectedR is not None:
            index = self.label_nameR.index(self.selectedR)
            move_label = self.labelsR[index]
            move_label_name = self.label_nameR[index]
            move_label_color = self.label_colorR[index]

            move_label_name.setStyleSheet("border: none; color: lightgray;")

            self.addLabelScrollL(move_label, move_label_name, move_label_color)

            self.labelsR.pop(index)
            self.createAllLabels(False)


    @pyqtSlot()
    def addLabelScrollR(self, new_label, new_label_name, new_label_color):

        scroll = None
        labels_layout = None
        labels = None
        label_name = None
        label_color = None

        scroll = self.scrollR
        labels_layout = self.labels_layoutR
        labels = self.labelsR
        label_name = self.label_nameR
        label_color = self.label_colorR


        label_layout = QHBoxLayout()
        label_layout.addWidget(new_label_color)
        label_layout.addWidget(new_label_name)

        labels_layout.addLayout(label_layout)


        tempWidget = QWidget()
        tempWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        tempWidget.setMinimumHeight(400)
        tempWidget.setMinimumWidth(220)
        tempWidget.setLayout(labels_layout)
        scroll.setWidget(tempWidget)

        labels.append(new_label)
        label_name.append(new_label_name)
        label_color.append(new_label_color)


    @pyqtSlot()
    def addLabelScrollL(self, new_label, new_label_name, new_label_color):
        scroll = None
        labels_layout = None
        labels = None
        label_name = None
        label_color = None

    
        scroll = self.scrollL
        labels_layout = self.labels_layoutL
        labels = self.labelsL
        label_name = self.label_nameL
        label_color = self.label_colorL

        index = bisect.bisect_left(labels, new_label)
        labels.insert(index, new_label)
        label_name.insert(index, new_label_name)
        label_color.insert(index, new_label_color)

        label_layout = QHBoxLayout()
        label_layout.addWidget(new_label_color)
        label_layout.addWidget(new_label_name)

        labels_layout.insertLayout(index, label_layout)

        tempWidget = QWidget()
        tempWidget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        tempWidget.setMinimumHeight(400)
        tempWidget.setMinimumWidth(220)
        tempWidget.setLayout(labels_layout)
        scroll.setWidget(tempWidget)

    
    def createAnnotation(self):
        self.create.emit(self.labelsR)

        self.close()





