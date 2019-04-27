
from commons.GenUtils import GenUtils
from commons.helpers import *
from angular5.ang_gen import AngGen

modelFile = '../model/users.ent'
from commons.BaseGen import  BaseGen


utils = GenUtils()


class IonicGen(AngGen):
    pass


if __name__ == "__main__":
    IonicGen().main()