class Label(object):
    """
    Label holds information about a classification.
    """

    def __init__(self, id, name, description = None, fill = [255, 255, 255], border = [200, 200, 200], visible = True):

        # id can be a string (for human readable convenience)
        # name is what the user will see on the interface
        # fill, and border are colors [r,g,b]

        self.id = id              # unique, can't change ever. eg. 'pocillopora'
        self.name = name          # human friendly label for a label eg. Pocillopora Putrescenses
        self.description = None
        self.fill = fill
        self.border = border
        self.visible = True

    def __lt__(self, other):
        return self.name < other.name


    def save(self):

        return self.__dict__

