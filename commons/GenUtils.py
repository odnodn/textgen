import typing
import stringcase

import configparser
import os
config = configparser.ConfigParser()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.ini')

class GenUtils:

    def __init__(self):
        config.read(CONFIG_PATH)
        for key in config: print(key)
        print(config)


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

    def getEnumProps(self, e):
        return [a for a in self.allProps(e) if self.isEnum(a)]

    def getAllSimpleProps(self, e):
        return [a for a in self.allProps(e) if self.isSimple(a) or self.isEnum(a)]

    def allSingleProps(self, e):
        return [a for a in self.allProps(e) if not a.many]

    def getOutgoingRefs(self, e):
        return [a for a in self.allProps(e) if self.isReference(a)]

    def getContained(self, e):  #e.g orderItems in an order or drugs in a prescription
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
        return self.isPropInTypes( property, ['int','currency', 'double'] )

    def prefix(self): return ''

    @staticmethod
    def humanize( str):
        return stringcase.sentencecase(str)

    @staticmethod
    def toFirstLower( name):
        return name if name == '' else name[0].lower() + name[1:]

    @staticmethod
    def toFirstUpper( name):
        return name if name == ''  else name[0].upper() + name[1:]

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

    def getTopLevelPackage(self):
        return 'com.abc.travelquote'
        #TODO return config['DEFAULT']['topLevelPackage']

    def getPackName(self, topLevelPackage, pck,stem, entity):
        return f'{topLevelPackage}.{pck.name}.{stem}.{entity.name}{toFirstUpper(stem)}'

    def getFqn(self, entity, stem=""):
        return f'{self.getTopLevelPackage()}.{entity.parent.name}.{entity.name}{self.toFirstUpper(stem)}'

    def getTestData(self, prop):
        if self.isEnum(prop) :
            return "random(" + self.getFqn(prop.type) + ".class)"
        elif (self.isPropOfType(prop ,"date")) :
            return 'randomDate("2011-04-15", "2011-11-07", new SimpleDateFormat("yyyy-MM-dd"))'
        elif(self.isPropOfType(prop ,"bool")):
            return"random(true, false)"
        elif(self.isPropOfType(prop ,"currency")) :
            return "random(Long.class, range(1, 10))" #todo should return bigdecimal
        elif(self.isPropOfType(prop ,"int")):
            return  "random(Integer.class, range(1, 200))"
        # elif(self.isPropOfType(prop ,"date"))   :
        #   "random(Long.class, range(1L, 100L))"
        else :	    #"string  #todo should return blurb for  large text
            return  "random(getUniqueNames())";