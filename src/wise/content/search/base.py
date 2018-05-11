from zope.component import queryMultiAdapter
from zope.interface import implements

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import interfaces
from z3c.form.button import buttonAndHandler
from z3c.form.field import Fields
from z3c.form.form import Form


class BaseFormUtil(object):
    """ Generic utilities for search views
    """

    def labelAsTitle(self, text):
        text = text.replace('_', ' ')

        for l in range(len(text)-1):
            if text[l].islower() and text[l + 1].isupper():
                text = text[:(l+1)] + ' ' + \
                    text[(l+1):]

        return text

    def get_marine_unit_id(self):
        parent = self.parentForm

        while True:
            muid = parent.data.get('marine_unit_id')

            if muid:
                break
            else:
                parent = parent.parentForm

        return muid


class SubForm(Form):
    implements(interfaces.ISubForm)
    ignoreContext = True

    template = ViewPageTemplateFile('pt/subform.pt')
    subform_class = None

    def __init__(self, context, request, parentForm):
        self.context = context
        self.request = request
        self.parentForm = self.__parent__ = parentForm
        self.data = {}

    def update(self):
        super(SubForm, self).update()

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

        return klass(self.context, self.request, self)

    def extras(self):
        extras = queryMultiAdapter((self, self.request), name='extras')

        if extras:
            return extras()


class ItemDisplayForm(SubForm):
    """ Generic form for displaying records
    """

    implements(interfaces.IItemDisplayForm)

    fields = Fields(interfaces.IRecordSelect)

    data_template = ViewPageTemplateFile('pt/item-display.pt')
    extra_data_template = ViewPageTemplateFile('pt/extra-data.pt')

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

    def update(self):
        super(ItemDisplayForm, self).update()
        self.data['page'] = self.widgets['page'].value
        self.set_item()

    def set_item(self):
        """ Compute the item to be displayed
        """

        # res = self.get_db_results()
        self.item = self.get_db_results()
        #
        # try:
        #     values = next(res)      # TODO: what if it's empty value?
        # except StopIteration:
        #     self.item = {}
        # else:
        #     keys = res.keys()
        #     self.item = dict(zip(keys, values))

    def get_extra_data(self):
        return []

    def extras(self):
        return self.extra_data_template()


class ItemDisplay(BrowserView, BaseFormUtil):
    """ A not-registered view that will render inline (a database result)
    """

    index = ViewPageTemplateFile('pt/simple-item-display.pt')
    data_template = ViewPageTemplateFile('pt/item-display.pt')
    extra_data_template = ViewPageTemplateFile('pt/extra-data.pt')
    data = {}

    def __init__(self, context, request):
        self.parentForm = context
        self.context = context
        self.request = request

    def __call__(self):
        self.set_item()

        return self.index()

    def get_db_results(self):
        raise NotImplementedError

    def get_page(self):
        page = self.parentForm.data.get('page')

        if page:
            return int(page)
        else:
            return 0

    def set_item(self):
        """ Compute the item to be displayed
        """

        res = self.get_db_results()

        try:
            values = next(res)      # TODO: what if it's empty value?
        except StopIteration:
            self.item = {}
        else:
            keys = res.keys()
            self.item = dict(zip(keys, values))

    def get_extra_data(self):
        return []

    def extras(self):
        return self.extra_data_template()


class MultiItemDisplayForm(SubForm):
    data_template = ViewPageTemplateFile('pt/multi-item-display.pt')

    fields = Fields(interfaces.IRecordSelect)

    def updateWidgets(self, prefix=None):
        super(MultiItemDisplayForm, self).updateWidgets()
        self.widgets['page'].mode = 'hidden'

    @buttonAndHandler(u'Prev', name='prev')
    def handle_prev(self, action):
        value = int(self.widgets['page'].value)
        self.widgets['page'].value = max(value - 1, 0)

    @buttonAndHandler(u'Next', name='next')
    def handle_next(self, action):
        value = int(self.widgets['page'].value)
        self.widgets['page'].value = value + 1

    def update(self):
        super(MultiItemDisplayForm, self).update()
        self.data['page'] = self.widgets['page'].value
