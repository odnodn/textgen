"""
An example how to generate java code from textX model using jinja2
template engine (http://jinja.pocoo.org/docs/dev/)
"""
from os import mkdir
from os.path import exists, dirname, join
import jinja2
from entity_test import get_entity_mm

#from textx.model import typ

class GenUtils:

    def __init__(self):
        self.myvar = 'sample_var'

    def isSimple (self, property):
        return property.type.name == 'entity.SimpleType'

    def toFirstLower(self, name):
        return name[0].lower() + name[1:]


def main(debug=False):

    this_folder = dirname(__file__)

    entity_mm = get_entity_mm(debug)

    # Build Person model from person.ent file
    person_model = entity_mm.model_from_file(join(this_folder, 'person.ent'))

    print(person_model)


    def alchemyTypes(s):
        """
        Maps type names from PrimitiveType to Java.
        """
        return {
                'integer': 'Integer',
                'string': 'String',
                'date' : 'Date',
                'bool' : 'Boolean'
        }.get(s.name, s.name)

    # Create output folder
    srcgen_folder = join(this_folder, 'srcgen')
    if not exists(srcgen_folder):
        mkdir(srcgen_folder)

    # Initialize template engine.
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(this_folder),
        trim_blocks=True,
        lstrip_blocks=True)

    # Register filter for mapping Entity type names to Java type names.
    jinja_env.filters['altype'] = alchemyTypes

    # Load Java template
    template = jinja_env.get_template('sqlalchemy.template')

    with open(join(srcgen_folder,
                   "%s.py" % 'model'), 'w') as f:
        f.write(template.render(model=person_model, genUtils = GenUtils() ))

    # for entity in person_model.entities:
    #     # For each entity generate java file
    #     with open(join(srcgen_folder,
    #                    "%s.py" % entity.name.capitalize()), 'w') as f:
    #         f.write(template.render(entity=entity))


if __name__ == "__main__":
    main()
