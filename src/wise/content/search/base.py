import datetime

from six import string_types
from sqlalchemy import inspect
from zope.component import queryMultiAdapter
from zope.interface import implements

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import interfaces
from z3c.form.button import buttonAndHandler
from z3c.form.field import Fields
from z3c.form.form import Form

from .utils import get_registered_form_sections


class BaseUtil(object):
    """ Generic utilities for search views
    """

    value_template = ViewPageTemplateFile('pt/value-display.pt')

    def name_as_title(self, text):
        """ Given a "CamelCase" text, changes it to "Title Text"

        This is used to transform the database column names to usable labels
        """
        text = text.replace('_', ' ')

        for l in range(len(text)-1):
            if text[l].islower() and text[l + 1].isupper():
                text = text[:(l+1)] + ' ' + \
                    text[(l+1):]

        return text

    def get_marine_unit_ids(self):
        """ Return the selected ids by looking up for data in parent forms
        """

        parent = self

        while True:
            ids = parent.data.get('marine_unit_ids')

            if ids:
                break
            else:
                parent = parent.context

        return ids

    def get_marine_unit_id(self):
        """ Return the current selected MarineUnitID looking up data in parents
        """

        parent = self

        while True:
            mid = parent.data.get('marine_unit_id')

            if mid:
                break
            else:
                parent = parent.context

        return mid

    def get_obj_fields(self, obj):
        """ Inspect an SA object and return its field names
        """
        mapper = inspect(obj)

        return [c.key for c in mapper.attrs]

    def print_value(self, value):
        if not value:
            return value
        base_values = string_types + (int, datetime.datetime, list)

        if not isinstance(value, base_values):

            return self.value_template(item=value)

        return value


class EmbededForm(Form, BaseUtil):
    """ Our most basic super-smart-superclass for forms

    It can embed other children forms
    """

    implements(interfaces.IEmbededForm)
    ignoreContext = True

    template = ViewPageTemplateFile('pt/subform.pt')
    subform_class = None

    def __init__(self, context, request):
        super(EmbededForm, self).__init__(context, request)
        self.__parent__ = self.context = context
        self.request = request
        self.data = {}

    def update(self):
        super(EmbededForm, self).update()

        self.data, errors = self.extractData()

        if not errors and not (None in self.data.values()):
            subform = self.get_subform()

            if subform is not None:
                self.subform = subform

    def get_subform(self, klass=None):
        if klass is None:
            klass = self.subform_class

        if klass is None:
            return None

        return klass(self, self.request)

    def extras(self):
        extras = queryMultiAdapter((self, self.request), name='extras')

        if extras:
            return extras()


class ItemDisplayForm(EmbededForm):
    """ Generic form for displaying records
    """

    implements(interfaces.IItemDisplayForm)

    fields = Fields(interfaces.IRecordSelect)

    template = ViewPageTemplateFile('pt/item-display-form.pt')
    data_template = ViewPageTemplateFile('pt/item-display.pt')
    extra_data_template = ViewPageTemplateFile('pt/extra-data.pt')

    def update(self):
        super(ItemDisplayForm, self).update()
        self.data['page'] = self.widgets['page'].value
        self.count, self.item = self.get_db_results()

    def updateWidgets(self, prefix=None):
        super(ItemDisplayForm, self).updateWidgets()
        self.widgets['page'].mode = 'hidden'

    @buttonAndHandler(u'Prev', name='prev')
    def handle_prev(self, action):
        value = int(self.widgets['page'].value)
        self.widgets['page'].value = max(value - 1, 0)

    @buttonAndHandler(u'Next', name='next')
    def handle_next(self, action):
        value = int(self.widgets['page'].value)
        self.widgets['page'].value = value + 1

    def get_extra_data(self):
        return []

    def extras(self):
        return self.extra_data_template()

    def get_page(self):
        page = self.data.get('page')

        if page:
            return int(page)
        else:
            return 0


class MultiItemDisplayForm(ItemDisplayForm):
    template = ViewPageTemplateFile('pt/multi-item-display.pt')

    fields = Fields(interfaces.IRecordSelect)

    # def update(self):
    #     super(MultiItemDisplayForm, self).update()
    #     self.data['page'] = self.widgets['page'].value
    #
    # def updateWidgets(self, prefix=None):
    #     super(MultiItemDisplayForm, self).updateWidgets()
    #     self.widgets['page'].mode = 'hidden'

    # @buttonAndHandler(u'Prev', name='prev')
    # def handle_prev(self, action):
    #     value = int(self.widgets['page'].value)
    #     self.widgets['page'].value = max(value - 1, 0)
    #
    # @buttonAndHandler(u'Next', name='next')
    # def handle_next(self, action):
    #     value = int(self.widgets['page'].value)
    #     self.widgets['page'].value = value + 1

    def get_sections(self):
        klasses = get_registered_form_sections(self)
        views = [k(self, self.request) for k in klasses]

        return views


class ItemDisplay(BrowserView, BaseUtil):
    """ A not-registered view that will render inline (a database result)
    """

    index = ViewPageTemplateFile('pt/simple-item-display.pt')

    data_template = ViewPageTemplateFile('pt/item-display.pt')
    extra_data_template = ViewPageTemplateFile('pt/extra-data.pt')

    data = {}

    def __init__(self, context, request):
        self.__parent__ = self.context = context
        self.request = request

    def __call__(self):
        self.count, self.item = self.get_db_results()

        return self.index()

    def get_db_results(self):
        raise NotImplementedError

    def get_page(self):
        page = self.context.data.get('page')

        if page:
            return int(page)
        else:
            return 0

    def get_extra_data(self):
        return []

    def extras(self):
        return self.extra_data_template()


# class MultiItemSubform(MultiItemDisplayForm):
#     """ Base class for multi-item display forms.
#     """
#
