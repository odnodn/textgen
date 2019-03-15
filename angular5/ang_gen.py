
from commons.GenUtils import GenUtils
from commons.helpers import *

modelFile = '../model/users.ent'
from commons.BaseGen import  BaseGen


utils = GenUtils()
topLevelPackage = 'com.bfwg'

import jinja2
import os


class AngGen(BaseGen):

    types = {
        'integer': 'number',
        'int' : 'number',
        'string': 'string',
        'date' : 'Date',
        'bool' : 'boolean',
        'text' : 'string',
        'file':'string',
        'currency': 'number'
    }



    def getMyPath(self):
        return dirname(__file__)

    def currentFolder(self):
        return dirname(__file__)

    def massageOutputFileName(self, opFileName):
        return GenUtils.toFirstLower(opFileName)

    def doGenerate(self,  model):

        self.createJinjaEnv(self.currentFolder())

        lstTemplates = searching_all_files('templates')

        for pck in model.elements:

            for entity in utils.getAbstractEntities(pck):
                #print(f'-------{entity.name} --------')
                for t in lstTemplates:
                    self.temlateToFile(t, entity, pck, 'entity', ['model'])

            for entity in utils.getEntities(pck):
                for t in lstTemplates:
                    self.temlateToFile(t, entity, pck, 'entity')


if __name__ == "__main__":
    AngGen().main()
    # cmd = 'cp -r srcgen/ ~/dev/ang/src/app'
    # os.system(cmd)