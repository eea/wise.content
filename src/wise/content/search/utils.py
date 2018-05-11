from collections import defaultdict


def pivot_data(data, pivot):
    out = defaultdict(list)

    for row in data:
        d = dict(row)
        p = d.pop(pivot)
        out[p].append(d)

    return out


FORMS = {}                  # main chapter 1 article form classes
SUBFORMS = {}               # store subform references


def register_form(klass):
    FORMS[klass.prefix] = klass

    return klass


def register_subform(form_name, subform_name):
    def wrapper(klass):
        SUBFORMS[(form_name, subform_name)] = klass

        return klass

    return wrapper


def get_registered_subform(form):
    """ Get the subform for a "main" form. For ex: A81a selects Ecosystem
    """

    theme = form.data.get('theme')

    if theme:
        return SUBFORMS.get((form.prefix, theme))
