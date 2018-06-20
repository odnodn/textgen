"""
An example how to generate java code from textX model using jinja2
template engine (http://jinja.pocoo.org/docs/dev/)
"""



from commons.GenUtils import GenUtils
from commons.helpers import *

modelFile = '../model/ecomm.ent'
from commons.BaseGen import  BaseGen


utils = GenUtils()
topLevelPackage = 'com.bfwg'
import jinja2
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

    def temlateToFile(self, t, entity, pck, typename='entity', filterPacks=[]):

        lname= utils.toFirstLower(entity.name)

        filename: str = t.parts[len(t.parts) - 1].replace('.jinja2', '' )
        print (f' {filename} {typename}')
        print (entity.parent.name)
        if not filename.startswith(typename):
            return
        filename = filename.replace(typename + '$', entity.name )
        tname = str(t.parent).replace(typename + '$', lname )
        tname = tname.replace('templates/', '' )
        tname = tname.replace('package$', pck.name )
        stemPackName = tname.split('/')[len(tname.split('/')) - 1]  #TODO : wont work on windows


        #print(stemPackName)
        if(len(filterPacks) == 0 or stemPackName in filterPacks ) :
            template = self.jinja_env.get_template(str(t))
            packageName = f'{topLevelPackage}.{pck.name}.{stemPackName}'

            def createFqn(  extension, fileExtension = None):
                fileExtension = f'{utils.toFirstUpper(extension)}' if not fileExtension else fileExtension
                return f'{topLevelPackage}.{pck.name}.{extension}.{entity.name}{fileExtension}'

            out = template.render(pck = packageName, entity=entity, fqn = createFqn('model',' '),
                                  fqnRepo = createFqn('repository'),
                                  fqnService = createFqn('service'),
                                  name=entity.name, lname= lname, genUtils=utils )
            writeToFile(f'srcgen/{tname}',filename , out)




    def doGenerate(self,  model):

        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(dirname(__file__)),
            trim_blocks=True,
            lstrip_blocks=True)
        self.jinja_env.filters['altype'] = self.translateType
        # Initialize template engine.

        # Register filter for mapping Entity type names to Java type names.

        lstTemplates = searching_all_files('templates')

        for pck in model.elements:

            for entity in utils.getAbstractEntities(pck):
                print(f'-------{entity.name} --------')
                for t in lstTemplates:
                    self.temlateToFile(t, entity, pck, 'entity', ['model'])

            for entity in utils.getEntities(pck):
                print(f'-------{entity.name} --------')
                for t in lstTemplates:
                    self.temlateToFile(t, entity, pck, 'entity')

            for enum in utils.getEnums(model):
                print(enum.name)
                for t in lstTemplates:
                    self.temlateToFile(t, enum, pck, 'enum' , ['model'])


if __name__ == "__main__":
    JavaGen().main()
    cmd = 'cp -r srcgen/ ~/dev/ionic/angular-spring-starter/server/src/main/java/com/bfwg'
    os.system(cmd)