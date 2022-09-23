from PyQt5.QtCore import Qt,QSize, QEvent, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QWidget, QSizePolicy, QPushButton, QHeaderView
from pathlib import Path
import os
from source.Project import Project
from source.Image import Image
from source.Annotation import Annotation
from source.Shape import Layer


path = Path(__file__).parent.absolute()
imdir = str(path)
imdir = imdir.replace('source', '')

class QtLayersWidget(QTreeWidget):
    showImage = pyqtSignal(Image)
    toggleLayer = pyqtSignal(Layer, bool)
    showAnnotations = pyqtSignal(Image, Annotation, bool)
    deleteLayer = pyqtSignal(Image, Layer)

    def __init__(self, parent=None):
        super(QtLayersWidget, self).__init__(parent)

        self.setHeaderHidden(True)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.setMinimumWidth(300)
        self.setMinimumHeight(60)

        self.trash = QIcon(imdir+os.path.join("icons", "trash.png"))
        self.icon_eyeopen = QIcon(imdir+os.path.join("icons", "eye.png"))
        self.icon_eyeclosed = QIcon(imdir+os.path.join("icons", "cross.png"))
        self.itemChanged.connect(self.itemChecked)
        self.itemDoubleClicked.connect(self.itemClickedTwice)

        self.setColumnCount(2)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.header().setSectionResizeMode(1, QHeaderView.Fixed)
        self.header().setStretchLastSection(False)
        self.setColumnWidth(1, 24)

        self.changedName = False

        #self.current_images = None

    def setProject(self, project):

        #if self.current_images == project.images:
        #    return

        #self.current_images = project.images.copy()

        self.blockSignals(True)
        self.clear()

        #items = []

        for image in project.images:
            item = QTreeWidgetItem()
            item.setText(0, image.name)
            item.setIcon(0, self.icon_eyeclosed)
            item.setCheckState(0, Qt.Unchecked)
            item.setExpanded(True)

            item.type = 'image'
            item.image = image

            for annotation in image.annotationLayers:
                child = QTreeWidgetItem()
                child.setText(0, annotation.name)
                child.setCheckState(0, Qt.Checked)
                child.setFlags(Qt.NoItemFlags)
                child.type = 'annotations'
                child.image = image
                child.annotation = annotation
                item.addChild(child)


            for layer in image.layers:
                child = QTreeWidgetItem()
                child.setText(0, layer.name)
                if layer.isEnabled():
                    child.setCheckState(0, Qt.Checked)
                else:
                    child.setCheckState(0, Qt.Unchecked)
                child.setFlags(Qt.NoItemFlags)
                child.type = 'layer'
                child.layer = layer
                child.image = image


                item.addChild(child)
                # ui->treeWidget->setItemWidget(items.value(1),0,new QPushButton("Click Me")); // Solution for your problem

            item.setExpanded(True)
            #items.append(item)
            self.addTopLevelItem(item);

        it = QTreeWidgetItemIterator(self)
        while it.value():
            item = it.value()
            if item.type == 'layer':
                image = item.image
                layer = item.layer
                type = item.type
                button = QPushButton()
                button.setIcon(self.trash)
                #button.setFixedWidth(100)
                button.clicked.connect(lambda x: self.deleteLayer.emit(image, layer))
                self.setItemWidget(item, 1, button)
            it += 1

        self.blockSignals(False)

    def setImage(self, image1, image2 = None):

        self.blockSignals(True)
        it = QTreeWidgetItemIterator(self)
        while it.value():
            imgWasChecked = False
            item = it.value()
            if item.type == 'image':
                if item.image == image1 or item.image == image2:
                    if item.checkState(0) != Qt.Checked:
                        item.setIcon(0, self.icon_eyeopen)
                        item.setCheckState(0, Qt.Checked)
                        #if len(item.image.layers):
                        #    item.setExpanded(True)
                        item.setExpanded(True)
                    else:
                        imgWasChecked = True 
                else:
                    item.setIcon(0, self.icon_eyeclosed)
                    item.setCheckState(0, Qt.Unchecked)
                    item.setExpanded(True)

                if image2 == None:
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                else:
                    item.setFlags( Qt.ItemIsEnabled)

                for i in range(item.childCount()):
                    child = item.child(i)
                    if item.image == image1 or item.image == image2:
                        child.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsEditable)
                    else:
                        child.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled | Qt.ItemIsEditable) #Qt.ItemIsEnabled)

                    if not imgWasChecked:   # if img was checked leave everything as before
                        child.setCheckState(0, Qt.Unchecked)

            it += 1

        self.blockSignals(False)

    def setAnnotations(self, itemChanged):
        self.blockSignals(True)

        it = QTreeWidgetItemIterator(self)
        while it.value():
            item = it.value()
            if item.type == 'image' and itemChanged.image == item.image:
                for i in range(item.childCount()):
                    child = item.child(i)
                    if child.type == 'annotations':
                        if child.annotation != itemChanged.annotation:
                            child.setCheckState(0, Qt.Unchecked)


            it += 1

        self.blockSignals(False)



    def itemChecked(self, item):
        checked = item.checkState(0) == Qt.Checked
        if item.type == 'image':
            self.setImage(item.image)
            self.showImage.emit(item.image)

        elif item.type == 'layer':
            self.toggleLayer.emit(item.layer, checked)

        elif item.type == 'annotations':
            if self.changedName:
                item.annotation.name = item.text(0)
                self.changedName = False
            checkedParent = item.parent().checkState(0) == Qt.Checked   
            if checkedParent:
                self.setAnnotations(item)
                self.showAnnotations.emit(item.image, item.annotation, checked)

    def itemClickedTwice(self, item):
        if item.type == 'annotations':
            self.editItem(item)
            self.changedName = True
        
