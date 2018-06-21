"""
An example how to generate java code from textX model using jinja2
template engine (http://jinja.pocoo.org/docs/dev/)
"""
from os import mkdir
import os
from os.path import exists, dirname, join
#from entity_test import  get_entity_mm
import jinja2
import copy
#from textx.metamodel import Property
from commons.GenUtils import GenUtils

from pathlib import Path


from textx.metamodel import metamodel_from_file


this_folder = dirname(__file__)

modelFile = '../model/users.ent'
metaModel = '../metamodel/entity.tx'
ex = 'ts'
utils = GenUtils()

def writeToFile(dr, fl, txt):
    DATA_DIR = Path(dr)
    DATA_DIR.mkdir(exist_ok=True, parents=True)
    FNAME = DATA_DIR.joinpath(Path(fl).name)
    FNAME.write_text(txt)

from pprint import pprint

def searching_all_files(directory):
    dirpath = Path(directory)
    assert(dirpath.is_dir())
    file_list = []
    for x in dirpath.iterdir():
        if x.is_file():
            file_list.append(x)
        elif x.is_dir():
            file_list.extend(searching_all_files(x))
    return file_list




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


def get_entity_mm( metaModel, debug=False,):

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

    entity_mm = get_entity_mm( metaModel, debug)

    # Build Person model from experiments.ent file
    model = entity_mm.model_from_file(join(this_folder, modelFile))

    for pck in model.elements:
        for entity in  utils.typeSelect(pck, 'Entity'):
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

    writeFile(this_folder, srcgen_folder, model, ['list-ts'])


def alchemyTypes(s):
    """
    Maps type names from PrimitiveType to Java.
    """
    types =  {
        'integer': 'number',
        'int' : 'number',
        'string': 'string',
        'date' : 'Date',
        'bool' : 'Boolean',
        'text' : 'string',
        'currency': 'number'
    }

    if type(s).__name__ == 'Enum': #its an enum
        return s.name

    return types.get(s.name, s.name)

def writeFile(this_folder, srcgen_folder, model, templates):
    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True,
        lstrip_blocks=True)

    # Register filter for mapping Entity type names to Java type names.
    jinja_env.filters['altype'] = alchemyTypes
    jinja_env.filters['fLower'] = GenUtils.toFirstLower
    jinja_env.filters['fUpper'] = GenUtils.toFirstUpper
    jinja_env.filters['plural'] = GenUtils.asCollection


    lstTemplates = searching_all_files('templates')


    for pck in model.elements:
        for entity in  utils.typeSelect(pck, 'Entity'):
            lname= utils.toFirstLower(entity.name)
            for t in lstTemplates:
                filename = t.parts[len(t.parts) - 1].replace('.jinja2', '' )
                filename = filename.replace('entity$', lname )
                tname = str(t.parent).replace('entity$', lname )
                tname = tname.replace('templates/', '' )
                print(tname)
                template = jinja_env.get_template(str(t))
                out = template.render(entity=entity, name=entity.name, lname= lname, genUtils=utils )
                writeToFile(f'srcgen/{tname}',filename , out)

        for enum in utils.getEnums(model):
            print(enum.name)
            for t in lstTemplates:
                self.temlateToFile(t, enum, pck, 'enum' , ['model'])


if __name__ == "__main__":
    main()
    cmd = 'cp -r srcgen/ ~/dev/angforms/src/app'
    os.system(cmd)
