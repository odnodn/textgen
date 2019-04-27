
from commons.GenUtils import GenUtils
from commons.helpers import *
from angular5.ang_gen import AngGen


from commons.BaseGen import  BaseGen


utils = GenUtils()


class IonicGen(AngGen):

    def currentFolder(self):
        return dirname(__file__)


if __name__ == "__main__":
    IonicGen().main()