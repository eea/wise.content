# from collections import defaultdict

from zope.schema import Choice

from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import db, interfaces, sql
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.button import buttonAndHandler
from z3c.form.field import Fields
from z3c.form.form import Form

from .base import (EmbededForm, ItemDisplay, ItemDisplayForm,
                   MarineUnitIDSelectForm, MultiItemDisplayForm)
from .utils import (get_form, pivot_data, register_form, register_form_section,
                    register_subform)
from .vocabulary import SubFormsVocabulary


class StartArticle8910Form(Form):
    """ Select the memberstate, region, area form
    """

    fields = Fields(interfaces.IStartArticles8910)

    fields['member_states'].widgetFactory = CheckBoxFieldWidget
    fields['region_subregions'].widgetFactory = CheckBoxFieldWidget
    fields['area_types'].widgetFactory = CheckBoxFieldWidget

    ignoreContext = True
    template = ViewPageTemplateFile('pt/mainform.pt')

    @buttonAndHandler(u'Apply filters', name='continue')
    def handle_continue(self, action):
        pass

    @buttonAndHandler(u'Download as XLS', name='download')
    def handle_download(self, action):
        # TODO: implement this, generalize this class as a superclass
        # TODO: implement download method here
        pass

    def update(self):
        super(StartArticle8910Form, self).update()

        self.data, errors = self.extractData()

        if not errors and all(self.data.values()):
            self.subform = MarineUnitIDsForm(self, self.request)


StartArticle8910View = wrap_form(StartArticle8910Form)


class MarineUnitIDsForm(EmbededForm):
    """ Select the MarineUnitID based on MemberState, Region and Area
    """

    fields = Fields(interfaces.IMarineUnitIDsSelect)

    def get_subform(self):
        return ArticleSelectForm(self, self.request)


class ArticleSelectForm(EmbededForm):
    """ Select one of the article: 8(a,b,c,d)/9/10
    """

    fields = Fields(interfaces.IArticleSelect)

    def get_subform(self):
        klass = get_form(self.data['article'])

        return super(ArticleSelectForm, self).get_subform(klass)


@register_form
class A9Form(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 9 form
    """

    title = 'Article 9 (GES determination)'
    mapper_class = sql.MSFD9Descriptor

    def get_subform(self):
        return A9ItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


class A9ItemDisplay(ItemDisplayForm):
    """ The implementation for the Article 9 (GES determination) form
    """
    extra_data_template = ViewPageTemplateFile('pt/extra-data-pivot.pt')

    mapper_class = sql.MSFD9Descriptor
    order_field = 'MSFD9_Descriptor_ID'

    def get_extra_data(self):
        if not self.item:
            return {}

        desc_id = self.item.MSFD9_Descriptor_ID

        res = db.get_a9_feature_impacts(desc_id)
        res = pivot_data(res, 'FeatureType')

        return [
            ('Feature Types', res)
        ]


@register_form
class A10Form(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 10 form
    """

    title = 'Article 10 (Targets)'
    mapper_class = sql.MSFD10Target

    def get_subform(self):
        return A10ItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


class A10ItemDisplay(ItemDisplayForm):
    """ The implementation of the Article 10 fom
    """
    mapper_class = sql.MSFD10Target
    order_field = 'MSFD10_Target_ID'

#     # TODO: the MSFD10_DESCrit is not ORM mapped yet
#     # this query is not finished!!!!

    def get_extra_data(self):
        if not self.item:
            return {}

        target_id = self.item.MSFD10_Target_ID

        res = db.get_a10_feature_targets(target_id)
        ft = pivot_data(res, 'FeatureType')

        return [
            ('Feature Type', ft),
        ]


@register_form
class A81aForm(EmbededForm):
    """ Main form for A81a.

    Allows selecting between Ecosystem, Functional, etc
    """

    title = 'Article 8.1a (Analysis of the environmental status)'

    @property
    def fields(self):
        # TODO: could this be reimplemented with simple vocab?
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


@register_subform(A81aForm)
class A81aEcoSubForm(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 8.1a form
    """
    title = 'Ecosystem(s)'
    mapper_class = sql.MSFD8aEcosystem

    def get_subform(self):
        return A81aEcoItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


class A81aEcoItemDisplay(MultiItemDisplayForm):
    """ Group the multiple items together for A8.1a
    """
    mapper_class = sql.MSFD8aEcosystem
    order_field = 'MSFD8a_Ecosystem_ID'


@register_form_section(A81aEcoItemDisplay)
class A81aEcosystemPressures(ItemDisplay):
    title = 'Pressures and impacts'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8aEcosystemPressuresImpact,
                'MSFD8a_Ecosystem',
                self.context.item.MSFD8a_Ecosystem_ID
            )


@register_form_section(A81aEcoItemDisplay)
class A81aEcosystemAsessment(ItemDisplay):
    title = 'Status Asessment'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8aEcosystemStatusAssessment,
                'MSFD8a_Ecosystem',
                self.context.item.MSFD8a_Ecosystem_ID
            )

    def get_extra_data(self):
        if not self.item:
            return {}

        count, item = db.get_related_record(
            sql.MSFD8aEcosystemStatusIndicator,
            'MSFD8a_Ecosystem_StatusAssessment',
            self.item.MSFD8a_Ecosystem_StatusAssessment_ID
        )
        # ft = pivot_data(res, 'FeatureType')

        return [
            ('Status Indicator', {'Feature': item}),
        ]

# @register_subform(A81aForm)
# class A81aFunctionalGroupSubForm(MultiItemDisplayForm):
#     title = 'Functional group(s)'
