import os
import json

from source.QtSettingsWidget import QtSettingsWidget
from source.Annotation import Annotation
from source.Label import Label

class DecayAnnotation(Annotation):



    def __init__(self):
        super(DecayAnnotation,self).__init__()

        self.dictionary_name = ""
        self.dictionary_description = ""
        self.labels = {}

        settings_widget = QtSettingsWidget( os.getcwd())
        default_dict_decayAnnotatio = settings_widget.settings.value("default-dictionary",
                                                defaultValue="dictionaries/default_dictionary_decay_Annotation.json", type=str)
        
        self.loadDictionary(default_dict_decayAnnotatio)

    def loadDictionary(self, filename):

        f = open(filename)
        dictionary = json.load(f)
        f.close()

        self.dictionary_name = dictionary['Name']
        self.dictionary_description = dictionary['Description']
        labels = dictionary['Labels']

        self.labels = {}
        for label in labels:
            id = label['id']
            name = label['name']
            fill = label['fill']
            border = label['border']
            description = label['description']
            self.labels[name] = Label(id=id, name=name, fill=fill, border=border)





