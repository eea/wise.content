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

from .db import get_available_marine_unit_ids, get_item_by_marineunitid
from .interfaces import IMainForm
from .utils import get_registered_form_sections
from .widget import MarineUnitIDSelectFieldWidget


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

    def get_main_form(self):
        """ Crawl back form chain to get to the main form
        """

        context = self

        while not IMainForm.providedBy(context):
            context = context.context

        return context


class MainForm(Form):
    """ The main forms need to inherit from this clas
    """

    implements(IMainForm)
    template = ViewPageTemplateFile('pt/mainform.pt')
    ignoreContext = True
    reset_page = False

    main_forms = (
        ('msfd-c1', 'Article 8, 9 & 10 (2012 reporting exercise)'),
        ('msfd-c2', 'Article 11 (2014 reporting exercise)'),
        ('msfd-c3', 'Article 13 & 14 (2015 reporting exercise)'),
    )

    @buttonAndHandler(u'Apply filters', name='continue')
    def handle_continue(self, action):
        self.reset_page = True

    @buttonAndHandler(u'Download as XLS', name='download')
    def handle_download(self, action):
        # TODO: implement this, generalize this class as a superclass
        # TODO: implement download method here
        pass

    @property
    def title(self):
        return [x[1] for x in self.main_forms if x[0] == self.name][0]


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


class MarineUnitIDSelectForm(EmbededForm):
    """ Base form for displaying information for a single MarineUnitID
    """

    fields = Fields(interfaces.IMarineUnitIDSelect)
    fields['marine_unit_id'].widgetFactory = MarineUnitIDSelectFieldWidget
    mapper_class = None         # what type of objects are we focused on?

    def update(self):
        # Override the default to be able to have a default marine unit id
        super(EmbededForm, self).update()

        self.data, errors = self.extractData()

        if not errors and not (None in self.data.values()):
            subform = self.get_subform()

            if subform is not None:
                self.subform = subform

    def get_available_marine_unit_ids(self):
        assert self.mapper_class
        ids = self.get_marine_unit_ids()
        count, res = get_available_marine_unit_ids(
            ids, self.mapper_class
        )

        return [x[0] for x in res]


class ItemDisplayForm(EmbededForm):
    """ Generic form for displaying records
    """

    implements(interfaces.IItemDisplayForm)

    fields = Fields(interfaces.IRecordSelect)

    template = ViewPageTemplateFile('pt/item-display-form.pt')
    data_template = ViewPageTemplateFile('pt/item-display.pt')
    extra_data_template = ViewPageTemplateFile('pt/extra-data.pt')

    mapper_class = None     # This will be used to retrieve the item
    order_field = None      # This will be used to properly page between items

    def update(self):
        super(ItemDisplayForm, self).update()

        if not self.get_main_form().reset_page:
            self.data['page'] = self.widgets['page'].value
        else:
            self.widgets['page'].value = 0
            self.data['page'] = 0

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

    def get_db_results(self):
        page = self.get_page()
        muid = self.get_marine_unit_id()

        return get_item_by_marineunitid(self.mapper_class, self.order_field,
                                        marine_unit_id=muid, page=page)


class MultiItemDisplayForm(ItemDisplayForm):
    template = ViewPageTemplateFile('pt/multi-item-display.pt')

    fields = Fields(interfaces.IRecordSelect)

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
        self.count = 0
        self.item = None

    def __call__(self):
        res = self.get_db_results()

        if res:
            self.count, self.item = res

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
