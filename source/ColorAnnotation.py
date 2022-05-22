import os
import json

from source.QtSettingsWidget import QtSettingsWidget
from source.Annotation import Annotation
from source.Label import Label

class ColorAnnotation(Annotation):



    def __init__(self, labels = {}):
        super(ColorAnnotation,self).__init__()

        self.dictionary_name = ""
        self.dictionary_description = ""
        
        self.setDictionaryFromListOfLabels(labels)
