"""
An example how to generate java code from textX model using jinja2
template engine (http://jinja.pocoo.org/docs/dev/)
"""
from os import mkdir
from os.path import exists, dirname, join
#from entity_test import  get_entity_mm
import jinja2
import copy
#from textx.metamodel import Property
from commons.GenUtils import GenUtils

from textx.metamodel import metamodel_from_file


this_folder = dirname(__file__)

modelFile = '../model/ecomm.ent'
metaModel = '../metamodel/entity.tx'
ex = 'py'
utils = GenUtils()


class SimpleType(object):
    """
    We are registering user SimpleType class to support
    simple types (integer, string) in our entity models
    Thus, user doesn't need to provide integer and string
    types in the model but can reference them in attribute types nevertheless.
    """
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __str__(self):
        return self.name


def get_entity_mm(debug=False):

    """
    Builds and returns a meta-model for Entity language.
    """
    # Built-in simple types
    # Each model will have this simple types during reference resolving but
    # these will not be a part of `types` list of EntityModel.
    type_builtins = {
        'int': SimpleType(None, 'int'),
        'string': SimpleType(None, 'string'),
        'text': SimpleType(None, 'text'),
        'bool': SimpleType(None, 'bool'),
        'date': SimpleType(None, 'date'),
        'dateTime': SimpleType(None, 'dateTime'),
        'currency': SimpleType(None, 'currency')
    }
    entity_mm = metamodel_from_file(join(this_folder, metaModel),
                                    classes=[SimpleType],
                                    builtins=type_builtins,
                                    debug=debug)



    return entity_mm




def main(debug=False):

    this_folder = dirname(__file__)

    entity_mm = get_entity_mm(debug)

    # Build Person model from experiments.ent file
    model = entity_mm.model_from_file(join(this_folder, modelFile))

    for pck in model.elements:
        for entity in  pck.elements:
            print (type(entity).__name__)

    for pck in model.elements:
        for entity in  utils.typeSelect(pck, 'Entity'):
            print (type(entity).__name__)
            for p in entity.properties:
                pass

    for pck in model.elements:
        for entity in  utils.typeSelect(pck, 'Entity'):
            for encmp in [encmp for encmp in utils.typeSelect(pck, 'Entity') if encmp is not entity]:
                for propcmp in encmp.properties:
                    if propcmp.type == entity:
                        print ("found " + propcmp.name + " -> " + encmp.name + " " + entity.name)
                    # x = EntityModel()
                    # x.parent = entity
                    # x.type = encmp
                    # entity.properties.append(x)
                    #
                    # x.type  =
                    # entity.properties.append(x)

    # Create output folder
    srcgen_folder = join(this_folder, 'srcgen')
    if not exists(srcgen_folder):
        mkdir(srcgen_folder)

    writeFile(this_folder, srcgen_folder, model, ['models','factories', 'model_tests'])


def alchemyTypes(s):
    """
    Maps type names from PrimitiveType to Java.
    """
    #print (s.name )
    # if(s.name  is not 'SimpleType'):
    #     print (s.type.name
    #
    # if s.type and s.type.name == 'enum' :
    #     return 'Enum(' + s.type.name + ')'

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
    return True if prop.opt else False

def writeFile(this_folder, srcgen_folder, model, templates):
    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True, #strip lines
        lstrip_blocks=True)  #strip whitespace

    # Register filter for mapping Entity type names to Java type names.
    jinja_env.filters['altype'] = alchemyTypes
    jinja_env.filters['opt'] = optFilter


    for t in templates:
        template = jinja_env.get_template('templates/' + t + '.jinja2' )
        for pck in model.elements:
            dir = join(srcgen_folder, pck.name)
            md(dir)
            with open(join(dir,
                           "%s.%s" % (t, ex)), 'w') as f:
                f.write(template.render(model=pck, genUtils=utils ))

def md(directory):
    if not exists(directory):
        mkdir(directory)

if __name__ == "__main__":
    main()
