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

    def getParent(self, entity):
        return entity.superType  if entity.superType else None

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

    def getAllSimpleProps(self, e):
        return [a for a in self.allProps(e) if self.isSimple(a) or self.isEnum(a) ]

    def getOutgoingRefs(self, e):
        return [a for a in self.allProps(e) if self.isReference(a) ]

    def getContained(self, e):
        return [a for a in self.allProps(e) if self.isManyEmbedded(a) ]

    def displayName(self, entity):
        for p in entity.properties:
            if self.isPropOfType(p, 'string'):
                return p
        return entity.properties[0]

    def isPropOfType(self, property, typename):
        return property.type.name == typename

    def isPropInTypes(self, property, names):
        return property.type.name in names


    def isMetaPropOfType(self, property, name):
        return type(property.type).__name__ == name

    def isMetaPropInTypes(self, property, names):
        return type(property.type).__name__ in names

    def isSimple (self, property):
        return self.isMetaPropInTypes( property, ['SimpleType','Enum'] )

    def isReference (self, property):
        return not self.isSimple(property) and not property.many

    def isManyEmbedded(self, property):
        return not self.isSimple(property) and  property.many and property.embedded

    def isEnum (self, property):
        return type(property.type).__name__ == 'Enum'

    def isNumeric(self , property):
        return self.isPropInTypes( property, ['int','Currency', 'Double'] )

    def prefix(self): return ''

    #todo - change these to pipe
    @staticmethod
    def toFirstLower( name):
        return name[0].lower() + name[1:]

    @staticmethod
    def toFirstUpper( name):
        return name[0].upper() + name[1:]

    @staticmethod
    def asCollection(prop):
        return GenUtils.toFirstLower(prop.type.name) + 's'

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


    def getTestData( prop):
        if prop.type.isEnum() :
            return "random(" + prop.type.fqn() + ".class)"
        elif (prop.isType("Date")) :
            return 'randomDate("2011-04-15", "2011-11-07", new SimpleDateFormat("yyyy-MM-dd"))'
        elif ( prop.isType("boolean") or prop.isType("Boolean") ):
             "random(true, false)"
        elif (prop.isCurrency() or prop.isType("Double")) :
            return "random(Long.class, range(1, 10))" #todo should return bigdecimal
        elif  prop.isType("Integer") :
              return  "random(Integer.class, range(1, 200))"
        elif ( prop.isType("long")):
          "random(Long.class, range(1L, 100L))"
        else :	    #"string  #todo should return blurb for  large text
            "random(getUniqueNames())";