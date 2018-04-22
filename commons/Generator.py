from os import mkdir
from os.path import exists, dirname, join
from commons.simpleType import  SimpleType
from textx.metamodel import metamodel_from_file
import jinja2

class Generator:

    def __init__(self, utils, metaModel, modelFile, this_folder, ex):
        self.this_folder =  this_folder    #TODO pass it as anrguement
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.this_folder),
            trim_blocks=True, #strip lines
            lstrip_blocks=True)  #strip whitespace

        self.srcgen_folder = join(self.this_folder, 'srcgen')
        if not exists(self.srcgen_folder):
            mkdir(self.srcgen_folder)
        self.utils = utils
        self.metaModel = metaModel
        self.modelFile = modelFile

        entity_mm = self.get_entity_mm(False)
        # Build Person model from experiments.ent file
        self.model = entity_mm.model_from_file(join(self.this_folder, modelFile))
        self.ex = ex

    def get_entity_mm(self, debug=False):

        """
        Builds and returns a meta-model for Entity language.
        """
        type_builtins = {
            'int': SimpleType(None, 'int'),
            'string': SimpleType(None, 'string'),
            'text': SimpleType(None, 'text'),
            'bool': SimpleType(None, 'bool'),
            'date': SimpleType(None, 'date'),
            'dateTime': SimpleType(None, 'dateTime'),
            'currency': SimpleType(None, 'currency')
        }
        entity_mm = metamodel_from_file(join(self.this_folder, self.metaModel),
                                        classes=[SimpleType],
                                        builtins=type_builtins,
                                        debug=debug)
        return entity_mm

    def writeFile(self, this_folder, model, templates):
        # Initialize template engine.
        for t in templates:
            template = self.jinja_env.get_template('templates/' + t + '.jinja2' )
            for pck in model.elements:
                dir = join(self.srcgen_folder, pck.name)
                self.md(dir)
                with open(join(dir,
                               "%s.%s" % (t, self.ex)), 'w') as f:
                    f.write(template.render(model=pck, genUtils=self.utils ))

    def md(self, directory):
        if not exists(directory):
            mkdir(directory)
