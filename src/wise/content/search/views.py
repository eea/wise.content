from zope.schema import Choice

from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import db, interfaces
from z3c.form.button import buttonAndHandler
from z3c.form.field import Fields
from z3c.form.form import Form

from .base import (BaseFormUtil, ItemDisplay, ItemDisplayForm,
                   MultiItemDisplayForm, SubForm)
from .utils import (get_form, get_registered_form_sections, pivot_data,
                    register_form, register_form_section, register_subform)
from .vocabulary import SubFormsVocabulary


class MainForm(Form):
    fields = Fields(interfaces.IMain_Articles8910)

    ignoreContext = True
    template = ViewPageTemplateFile('pt/mainform.pt')

    @buttonAndHandler(u'Apply filters', name='continue')
    def handle_continue(self, action):
        pass

    def update(self):
        super(MainForm, self).update()

        self.data, errors = self.extractData()

        if not errors and all(self.data.values()):
            self.subform = MarineUnitIDForm(self, self.request, self)


SearchDemo = wrap_form(MainForm)


class ArticleSelectForm(SubForm):
    fields = Fields(interfaces.IArticleSelect)

    def get_subform(self):
        klass = get_form(self.data['article'])

        return super(ArticleSelectForm, self).get_subform(klass)


class MarineUnitIDForm(SubForm):
    fields = Fields(interfaces.IMarineUnitIDSelect)
    subform_class = ArticleSelectForm


@register_form
class A9Form(ItemDisplayForm, BaseFormUtil):
    title = 'Article 9 (GES determination)'
    fields = Fields(interfaces.IRecordSelect)

    def get_db_results(self):
        page = int(self.data.get('page')) or 0
        muid = self.get_marine_unit_id()
        res = db.get_a9_descriptors(marine_unit_id=muid, page=page)

        return res

    def get_extra_data(self):
        if not self.item:
            return {}

        desc_id = self.item['MSFD9_Descriptor_ID']

        res = db.get_a9_feature_impacts(desc_id)
        res = pivot_data(res, 'FeatureType')

        return [
            ('Feature Types', res)
        ]


@register_form
class A10Form(ItemDisplayForm, BaseFormUtil):
    title = 'Article 10 (Targets)'

    def get_db_results(self):
        page = int(self.data.get('page')) or 0
        muid = self.get_marine_unit_id()
        res = db.get_a10_targets(marine_unit_id=muid, page=page)

        return res

    def get_extra_data(self):
        if not self.item:
            return {}

        target_id = self.item['MSFD10_Target_ID']

        res = db.get_a10_feature_targets(target_id)
        ft = pivot_data(res, 'FeatureType')

        # res = db.get_a10_feature_targets(target_id)
        # criteria = pivot_data(res, 'FeatureType')

        return [
            ('Feature Types', ft),
            # ('Criteria Indicators', criteria),
        ]


@register_form
class A81aForm(SubForm):
    """ Main form for A81a.

    Allows selecting between Ecosystem, Functional, etc
    """

    title = 'Article 8.1a (Analysis of the environmental status)'

    @property
    def fields(self):
        # TODO: this can be reimplemented with simple vocab, no need for hard
        theme = Choice(
            __name__='theme',
            title=u"Select theme",
            required=False,
            vocabulary=SubFormsVocabulary(self.__class__)
        )

        return Fields(theme)

    def get_subform(self):
        klass = self.data.get('theme')

        return super(A81aForm, self).get_subform(klass)


class MultiItemSubform(MultiItemDisplayForm, BaseFormUtil):
    """ Base class for multi-item display forms.
    """

    def get_sections(self):
        klasses = get_registered_form_sections(self)
        views = [k(self, self.request) for k in klasses]

        return views


@register_subform(A81aForm)
class A81aEcoSubForm(MultiItemSubform):
    title = 'Ecosystem(s)'


@register_subform(A81aForm)
class A81aFunctionalGroupSubForm(MultiItemSubform):
    title = 'Functional group(s)'


@register_form_section(A81aEcoSubForm)
class A81aEcosystemPressures(ItemDisplay):
    title = 'Pressures and impacts'

    def get_db_results(self):
        page = self.get_page()
        muid = self.get_marine_unit_id()
        res = db.get_a10_targets(marine_unit_id=muid, page=page)

        return res

    def get_extra_data(self):
        if not self.item:
            return {}

        target_id = self.item['MSFD10_Target_ID']

        res = db.get_a10_feature_targets(target_id)
        ft = pivot_data(res, 'FeatureType')

        return [
            ('Feature Types', ft),
        ]
