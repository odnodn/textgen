from commons.GenUtils import GenUtils
from commons.helpers import *
from abc import ABC, abstractmethod
from os import mkdir

import jinja2

this_folder = dirname(__file__)
metaModel = '../metamodel/entity.tx'

import shutil



class BaseGen:

    def __init__(self):
        # self.jinja_env = jinja2.Environment(
        #     loader=jinja2.FileSystemLoader(self.getMyFolder()),
        #     trim_blocks=True,
        #     lstrip_blocks=True)
        # self.jinja_env.filters['altype'] = self.translateType
        print ('in init super')



    def main(self,debug=False):

        entity_mm = get_entity_mm(metaModel, debug)

        # Build Person model from experiments.ent file
        model = entity_mm.model_from_file(join(this_folder, self.getModelFile() ))

        # Create output folder
        srcgen_folder = join(this_folder, 'srcgen')

        shutil.rmtree(srcgen_folder)

        if not exists(srcgen_folder):
            mkdir(srcgen_folder)

        self.doGenerate( model)


    def translateType(self, s):
        """
        Maps type names from PrimitiveType to Java.
        """
        if type(s).__name__ == 'Enum': #its an enum
            return s.name

        return self.types.get(s.name, s.name)

    @abstractmethod
    def doGenerate(self):
        pass

    @abstractmethod
    def getModelFile(self):
        pass

    @abstractmethod
    def getMyFolder(self):
        pass