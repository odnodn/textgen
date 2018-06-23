
from commons.GenUtils import GenUtils
from commons.helpers import *

modelFile = '../model/users.ent'
from commons.BaseGen import  BaseGen


utils = GenUtils()
topLevelPackage = 'com.bfwg'

import jinja2
import os


class AngGen(BaseGen):

    types =  {
            'integer': 'number',
            'int' : 'number',
            'string': 'string',
            'date' : 'Date',
            'bool' : 'boolean',
            'text' : 'string',
            'currency': 'number'
        }

    def getModelFile(self):
        return modelFile

    def getMyPath(self):
        return dirname(__file__)

    #todo: merger this with java gen
    def doGenerate(self,  model):
        this_folder = dirname(__file__)
        self.createJinjaEnv(this_folder)

        lstTemplates = searching_all_files('templates')

        for pck in model.elements:

            for entity in utils.getAbstractEntities(pck):
                #print(f'-------{entity.name} --------')
                for t in lstTemplates:
                    self.temlateToFile(t, entity, pck, 'entity', ['model'])

            for entity in utils.getEntities(pck):
                for t in lstTemplates:
                    self.temlateToFile(t, entity, pck, 'entity')

            for enum in utils.getEnums(pck):
                print(enum.name)
                for t in lstTemplates:
                    self.temlateToFile(t, enum, pck, 'enum' )




if __name__ == "__main__":
    AngGen().main()
    cmd = 'cp -r srcgen/ ~/dev/angforms/src/app'
    os.system(cmd)
