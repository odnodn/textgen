def writeToFile(dr, fl, txt):
    DATA_DIR = Path(dr)
    DATA_DIR.mkdir(exist_ok=True, parents=True)
    FNAME = DATA_DIR.joinpath(Path(fl).name)
    FNAME.write_text(txt)

from pprint import pprint

def searching_all_files(directory):
    dirpath = Path(directory)
    assert(dirpath.is_dir())
    file_list = []
    for x in dirpath.iterdir():
        if x.is_file():
            file_list.append(x)
        elif x.is_dir():
            file_list.extend(searching_all_files(x))
    return file_list


class SimpleType(object):

    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __str__(self):
        return self.name


def get_entity_mm(debug=False):

    """
    Builds and returns a meta-model for Entity language.
    """
    # Built-in simple types
    # Each model will have this simple types during reference resolving but
    # these will not be a part of `types` list of EntityModel.
    type_builtins = {
        'int': SimpleType(None, 'int'),
        'string': SimpleType(None, 'string'),
        'text': SimpleType(None, 'text'),
        'bool': SimpleType(None, 'bool'),
        'date': SimpleType(None, 'date'),
        'dateTime': SimpleType(None, 'dateTime'),
        'currency': SimpleType(None, 'currency')
    }
    entity_mm = metamodel_from_file(join(this_folder, metaModel),
                                    classes=[SimpleType],
                                    builtins=type_builtins,
                                    debug=debug)



    return entity_mm
