"""
An example how to generate java code from textX model using jinja2
template engine (http://jinja.pocoo.org/docs/dev/)
"""



from commons.GenUtils import GenUtils
from commons.helpers import *

modelFile = '../model/users.ent'

from commons.BaseGen import  BaseGen


utils = GenUtils()

import os


class JavaGen(BaseGen):

    types =  {
        'integer': 'Integer',
        'int' : 'int',
        'string': 'String',
        'date' : 'Date',
        'bool' : 'boolean',
        'text' : 'String',
        'currency': 'BigDecimal'
    }

    def getModelFile(self):
        return modelFile

    def getMyPath(self):
        return dirname(__file__)

    def currentFolder(self):
        return dirname(__file__)



if __name__ == "__main__":
    JavaGen().main()
    cmd = 'cp -r srcgen/ ' + utils.getConfig('outputJava')  + utils.getTopLevelPackage().replace('.','/')
    os.system(cmd)