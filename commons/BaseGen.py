from commons.GenUtils import GenUtils
from commons.helpers import *
from abc import ABC, abstractmethod
from os import mkdir

import shutil

this_folder = dirname(__file__)
metaModel = '../metamodel/entity.tx'

#TODO: pass into functions
#topLevelPackage = 'com.bfwg'

import jinja2

utils = GenUtils()


class BaseGen:
    def __init__(self):
        # self.jinja_env = jinja2.Environment(
        #     loader=jinja2.FileSystemLoader(self.getMyFolder()),
        #     trim_blocks=True,
        #     lstrip_blocks=True)
        # self.jinja_env.filters['altype'] = self.translateType
        print('in init super')

    def main(self, debug=False):

        entity_mm = get_entity_mm(metaModel, debug)

        # Build Person model from experiments.ent file
        model = entity_mm.model_from_file(join(this_folder, self.getModelFile()))

        # Create output folder
        srcgen_folder = join(this_folder, 'srcgen')

        shutil.rmtree(srcgen_folder)

        if not exists(srcgen_folder):
            mkdir(srcgen_folder)

        self.doGenerate(model)

    def translateType(self, s):
        """
        Maps type names from PrimitiveType to the generator e.g java or angular .
        """
        if type(s).__name__ == 'Enum':  # its an enum
            return s.name

        return self.types.get(s.name, s.name)

    def createJinjaEnv(self, currentFolder):
        #this_folder = dirname(__file__)
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(currentFolder),
            trim_blocks=True,
            lstrip_blocks=True)
        self.jinja_env.filters['altype'] = self.translateType
        self.jinja_env.filters['fLower'] = GenUtils.toFirstLower
        self.jinja_env.filters['fUpper'] = GenUtils.toFirstUpper
        self.jinja_env.filters['plural'] = GenUtils.asCollection
        self.jinja_env.filters['humanize'] = GenUtils.humanize


    def doGenerate(self,  model):

        self.createJinjaEnv(self.currentFolder())

        lstTemplates = searching_all_files('templates')

        for pck in model.elements:

            for t in lstTemplates:
                self.temlateToFile(t, pck, pck, 'package')

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

    def temlateToFile(self, t, entity, pck, typename='entity', filterPacks=[]):

        lname= GenUtils.toFirstLower(entity.name)

        filename: str = t.parts[len(t.parts) - 1].replace('.jinja2', '' )

        # print('trying to load template ' + str(t))

        filename = filename.replace(typename + '$', entity.name)
        tname = self.getGeneratedFileName(entity, filename, lname, pck, t, typename)
        print(tname)

        if not filename.startswith(typename) and '$' in filename:
            return

        stemPackName = tname.split('/')[len(tname.split('/')) - 1]  #TODO : wont work on windows


        #print(stemPackName)
        if(len(filterPacks) == 0 or stemPackName in filterPacks ) :
            #print('trying to load template ' + str(t))
            template = self.jinja_env.get_template(str(t))
            packageName = f'{utils.getTopLevelPackage()}.{pck.name}.{stemPackName}'

            def createFqn(  extension, fileExtension = None):
                fileExtension = f'{GenUtils.toFirstUpper(extension)}' if not fileExtension else fileExtension
                return f'{utils.getTopLevelPackage()}.{pck.name}.{extension}.{entity.name}{fileExtension}'

            out = template.render(mdl = pck.parent, pck = packageName, entity=entity, fqn = createFqn('model',' '),
                                  fqnRepo = createFqn('repository'),
                                  fqnService = createFqn('service'),
                                  name=entity.name, lname= lname, genUtils=GenUtils() )
            writeToFile(f'srcgen/{tname}',self.massageOutputFileName(filename) , out)

    def getGeneratedFileName(self, entity, filename, lname, pck, t, typename):
        tname = str(t.parent).replace(typename + '$', lname)
        tname = tname.replace('templates/', '')
        tname = tname.replace('package$', pck.name)
        return tname



    #@abstractmethod
    def getModelFile(self)-> str :
       return  utils.getConfig('modelFile')

    @abstractmethod
    def currentFolder(self):
        pass

    @abstractmethod
    def massageOutputFileName(self, opFileName):
        return opFileName


