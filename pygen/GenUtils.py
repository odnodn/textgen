class GenUtils:

    def __init__(self):
        self.myvar = 'sample_var'

    def isSimple (self, property):
        name = type(property.type).__name__
        return name == 'SimpleType' or name == 'Enum'

    def isEnum (self, property):
        return type(property.type).__name__ == 'Enum'

    def prefix(self): return 'db.'


    def toFirstLower(self, name):
        return name[0].lower() + name[1:]

    def findBackRef(self, property):
        print(property.__class__.__name__)
        container = property.parent
        entity = property.type
        for propcmp in entity.properties:
            if propcmp.type == container:
                #print ("found " + propcmp.name + " -> " + encmp.name + " " + entity.name)
                return propcmp
