"""
An example how to generate java code from textX model using jinja2
template engine (http://jinja.pocoo.org/docs/dev/)
"""


#from entity_test import  get_entity_mm

import copy
#from textx.metamodel import Property
from commons.GenUtils import GenUtils
import os


from commons.Generator import Generator


#this_folder = dirname(__file__)

modelFile = '../model/ecomm.ent'
metaModel = '../metamodel/entity.tx'
ex = 'js'
utils = GenUtils()



def alchemyTypes(s):
    """
    Maps type names from PrimitiveType to Java.
    """

    types =  {
        'integer': 'Integer',
        'int' : 'Integer',
        'string': 'String',
        'date' : 'Date',
        'bool' : 'Boolean',
        'text' : 'Text',
        'currency': 'Numeric'
    }

    if(type(s).__name__ == 'Enum'): #its an enum
        return 'Enum(' + s.name + ')'

    return types.get(s.name, s.name)

def optFilter(prop):
    return 'true' if prop.opt else 'false'

def parentFilter(entity):
    return 'BaseSchema' if not entity.superType else entity.superType.name + 'Schema'


def dumpModel(model):
    for pck in model.elements:
        for entity in  pck.elements:
            print (type(entity).__name__ + ":" + entity.name)


def main(debug=False):

    generator = Generator(utils, metaModel, modelFile, os.path.dirname(__file__), ex)

    # Register filter for mapping Entity type names to Java type names.
    generator.jinja_env.filters['altype'] = alchemyTypes
    generator.jinja_env.filters['opt'] = optFilter
    generator.jinja_env.filters['parent'] = parentFilter


    dumpModel(generator.model)

    # Create output folder
    generator.writeFile(None, generator.model, ['models','factories', 'model_tests'])




if __name__ == "__main__":
    main()
