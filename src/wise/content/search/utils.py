from collections import defaultdict
from io import BytesIO

from sqlalchemy import inspect

import xlsxwriter


def pivot_data(data, pivot):
    out = defaultdict(list)

    for row in data:
        d = dict(row)
        p = d.pop(pivot)
        out[p].append(d)

    return out


FORMS = {}                         # main chapter 1 article form classes
SUBFORMS = defaultdict(set)        # store subform references
ITEM_DISPLAYS = defaultdict(set)   # store registration for item displays


def class_id(obj):
    if type(obj) is type:
        klass = obj
    else:
        klass = obj.__class__

    return klass.__name__.lower()


def register_form(klass):
    """ Registers a 'secondary' form class

    These are the forms implementing the 'Article 9 (GES determination)',
    'Article 10 (Targets)' and so on, for one of the 'chapters'.
    """

    FORMS[class_id(klass)] = klass

    return klass


def get_form(name):
    if name:
        return FORMS[name]


def register_subform(mainform):
    """ Registers a 'subform' as a possible choice for displaying data

    These are the 'pages', such as 'Ecosystem(s)', 'Functional group(s)' in the
    'Article 8.1a (Analysis of the environmental status)'
    """

    def wrapper(klass):
        SUBFORMS[mainform].add(klass)

        return klass

    return wrapper


def get_registered_subform(form, name):
    """ Get the subform for a "main" form. For ex: A81a selects Ecosystem
    """

    if name:
        return SUBFORMS.get((class_id(form), name))


def register_form_section(parent_klass):
    """ Registers a 'section' in a page with data.

    These are the 'sections' such as 'Pressures and impacts' or
    'Status assessment' in subform 'Ecosystem(s)' in 'Article 8.1a (Analysis of
    the environmental status)'
    """

    def wrapper(klass):
        ITEM_DISPLAYS[parent_klass].add(klass)

        return klass

    return wrapper


def get_registered_form_sections(form):
    return ITEM_DISPLAYS[form.__class__]


def scan(namespace):
    """ Scans the namespace for modules and imports them, to activate decorator
    """

    import importlib
    # import pkgutil
    # import wise.content.search

    name = importlib._resolve_name(namespace, 'wise.content.search', 1)
    importlib.import_module(name)


def data_to_xls(data):

    # Create a workbook and add a worksheet.
    out = BytesIO()
    workbook = xlsxwriter.Workbook(out, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    row0 = data[0]
    fields = sorted(get_obj_fields(row0))

    # write titles

    for i, f in enumerate(fields):
        worksheet.write(0, i, f)

    for j, row in enumerate(data):
        for i, f in enumerate(fields):
            # TODO: check value type
            value = unicode(getattr(row, f))
            worksheet.write(j + 1, i, value)

    workbook.close()
    out.seek(0)

    return out


def get_obj_fields(obj):
    mapper = inspect(obj)

    return [c.key for c in mapper.attrs]
