"""
An example how to generate java code from textX model using jinja2
template engine (http://jinja.pocoo.org/docs/dev/)
"""
from os import mkdir
from os.path import exists, dirname, join

import jinja2

from commons.GenUtils import GenUtils
from commons.helpers import *

this_folder = dirname(__file__)

modelFile = '../model/users.ent'
metaModel = '../metamodel/entity.tx'
ex = 'ts'
utils = GenUtils()
topLevelPackage = 'com.bfwg'

def main(debug=False):

    entity_mm = get_entity_mm(metaModel, debug)

    # Build Person model from experiments.ent file
    model = entity_mm.model_from_file(join(this_folder, modelFile))

    # Create output folder
    srcgen_folder = join(this_folder, 'srcgen')
    if not exists(srcgen_folder):
        mkdir(srcgen_folder)

    writeFile( model)


def alchemyTypes(s):
    """
    Maps type names from PrimitiveType to Java.
    """
    types =  {
        'integer': 'Integer',
        'int' : 'int',
        'string': 'String',
        'date' : 'Date',
        'bool' : 'boolean',
        'text' : 'String',
        'currency': 'BigDecimal'
    }

    if(type(s).__name__ == 'Enum'): #its an enum
        return  s.name

    return types.get(s.name, s.name)

def writeFile(  model):

    this_folder = dirname(__file__)
    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True,
        lstrip_blocks=True)

    # Register filter for mapping Entity type names to Java type names.
    jinja_env.filters['altype'] = alchemyTypes

    lstTemplates = searching_all_files('templates')


    for pck in model.elements:
        for entity in  utils.typeSelect(pck, 'Entity'):
            lname= utils.toFirstLower(entity.name)
            for t in lstTemplates:
                filename = t.parts[len(t.parts) - 1].replace('.jinja2', '' )
                filename = filename.replace('entity$', entity.name )
                tname = str(t.parent).replace('entity$', lname )
                tname = tname.replace('templates/', '' )
                tname = tname.replace('package$', pck.name )
                stemPackName = tname.split('/')[len(tname.split('/')) - 1]  #TODO : wont work on windows
                print(stemPackName)
                template = jinja_env.get_template(str(t))
                packageName = f'{topLevelPackage}.{pck.name}.{stemPackName}'
                fqn=f'{topLevelPackage}.{pck.name}.model.{entity.name}'
                fqnRepo = f'{topLevelPackage}.{pck.name}.repository.{entity.name}Repository'
                out = template.render(pck = packageName, entity=entity, fqn = fqn ,fqnRepo = fqnRepo,
                                      name=entity.name, lname= lname, genUtils=utils )
                writeToFile(f'srcgen/{tname}',filename , out)


if __name__ == "__main__":
    main()

#cp -r srcgen/users ~/dev/ionic/spring-petclinic-rest/src/main/java/org/springframework/samples/users
