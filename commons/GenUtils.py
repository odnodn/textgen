import typing
class GenUtils:

    def __init__(self):
        self.myvar = 'sample_var'

    def typeSelect(self, parent, name):
        return [e for e in parent.elements if type(e).__name__ == name]

    def getEnums(self, parent):
        return self.typeSelect(parent, 'Enum')

    def getEntities(self, parent):
        return [e for e in self.typeSelect(parent, 'Entity') if e.abs == False ]

    def getAbstractEntities(self, parent):
        return [e for e in self.typeSelect(parent, 'Entity') if e.abs == True ]

    def allProps(self, e):
        ps = []
        def recProps(e, ps):
            if(e.superType):
                 ps += e.superType.properties
                 return recProps(e.superType, ps)
            else:
                return ps
        ps =  recProps(e, ps)
        return ps + e.properties


    def displayName(self, entity):
        for p in entity.properties:
            if self.isPropOfType(p, 'string'):
                return p
        return entity.properties[0]

    def isPropOfType(self, property, name):
        return type(property.type).__name__ == name

    def isPropInTypes(self, property, names):
        return type(property.type).__name__ in names

    def isSimple (self, property):
        return self.isPropInTypes( property, ['SimpleType','Enum'] )

    def isEnum (self, property):
        return type(property.type).__name__ == 'Enum'

    def prefix(self): return ''


    def toFirstLower(self, name):
        return name[0].lower() + name[1:]

    def toFirstUpper(self, name):
        return name[0].upper() + name[1:]

    def findBackRef(self, property):
        print(property.__class__.__name__)
        container = property.parent
        entity = property.type
        for propcmp in entity.properties:
            if propcmp.type == container:
                #print ("found " + propcmp.name + " -> " + encmp.name + " " + entity.name)
                return propcmp

    def getPackName(self, topLevelPackage, pck,stem, entity):
        return f'{topLevelPackage}.{pck.name}.{stem}.{entity.name}{toFirstUpper(stem)}'

