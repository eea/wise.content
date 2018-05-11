
from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import db, interfaces
from z3c.form.button import buttonAndHandler
from z3c.form.field import Fields
from z3c.form.form import Form

from .base import BaseFormUtil, ItemDisplayForm, MultiItemDisplayForm, SubForm
from .utils import (FORMS, get_registered_subform, pivot_data, register_form,
                    register_subform)


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

        if all(self.data.values()):
            self.data['MarineUnitID'] = db.get_marine_unit_id(**self.data)

            if not errors and self.data['MarineUnitID']:
                self.subform = ArticleSelectForm(
                    self.context, self.request, self)

        if errors:
            self.status = self.formErrorsMessage

            return


SearchDemo = wrap_form(MainForm)


class ArticleSelectForm(SubForm):
    fields = Fields(interfaces.IArticleSelect)
    prefix = 'article_select'
    data = {}
    # subform_class = ArticleSelectForm

    def get_subform(self):
        klass = FORMS.get(self.data['article'])

        return super(ArticleSelectForm, self).get_subform(klass)


@register_form
class A9Form(ItemDisplayForm, BaseFormUtil):
    title = 'Article 9 (GES determination)'
    fields = Fields(interfaces.IRecordSelect)
    prefix = 'a9'

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
    fields = Fields(interfaces.IRecordSelect)
    prefix = 'a10'

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
    fields = Fields(interfaces.IA81aSubformSelect)
    prefix = 'a81a'     # prefix is important to identify available subforms
    data = {}

    def get_subform(self):
        klass = get_registered_subform(self)

        return super(A81aForm, self).get_subform(klass)


@register_subform('a81a', 'Ecosystem(s)')
class A81aEcoSubForm(MultiItemDisplayForm, BaseFormUtil):
    fields = Fields(interfaces.IRecordSelect)
    prefix = 'a81a_eco_subform'
    data = {}

    def get_db_results(self):
        page = int(self.data.get('page')) or 0
        muid = self.get_marine_unit_id()
        res = db.get_a10_targets(marine_unit_id=muid, page=page)

        return res

    # def get_extra_data(self):
    #     if not self.item:
    #         return {}
    #
    #     target_id = self.item['MSFD10_Target_ID']
    #
    #     res = db.get_a10_feature_targets(target_id)
    #     ft = pivot_data(res, 'FeatureType')
    #
    #     return [
    #         ('Feature Types', ft),
    #     ]
