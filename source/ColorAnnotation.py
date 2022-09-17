import os
import json

from source.QtSettingsWidget import QtSettingsWidget
from source.Annotation import Annotation
from source.Label import Label

class ColorAnnotation(Annotation):

    def __init__(self, name = "Color Annotation", id = -1, dictionary_name = "", dictionary_description = "", labels = {}):
        super(ColorAnnotation,self).__init__(name, id)

        self.name = name
        self.type = "ColorAnnotation"

        
        self.dictionary_name = dictionary_name
        self.dictionary_description = dictionary_description
        for label in labels:
            self.labels[label] = Label(**labels[label])


    def setDictionaryFromListOfLabels(self, name, description, labels):
        self.dictionary_name = name
        self.dictionary_description = description
        super(ColorAnnotation,self).setDictionaryFromListOfLabels(labels)
