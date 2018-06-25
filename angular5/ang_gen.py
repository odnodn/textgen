
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

    def currentFolder(self):
        return dirname(__file__)

    def massageOutputFileName(self, opFileName):
        return GenUtils.toFirstLower(opFileName)


if __name__ == "__main__":
    AngGen().main()
    cmd = 'cp -r srcgen/ ~/dev/angforms/src/app'
    os.system(cmd)
