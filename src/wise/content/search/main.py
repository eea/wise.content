
from plone.z3cform.layout import wrap_form
from wise.content.search import db, interfaces, sql
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.field import Fields

from .a11 import StartArticle11Form
from .a1314 import StartArticle1314Form
from .base import EmbededForm, MainForm, MainFormWrapper
from .utils import (all_values_from_field, default_value_from_field, get_form,
                    scan)


class StartArticle8910Form(MainForm):
    """ Select one of the article: 8(a,b,c,d)/9/10
    """

    name = 'msfd-c1'

    fields = Fields(interfaces.IArticleSelect)
    session_name = 'session'

    def get_subform(self):
        if self.data['article']:
            return RegionForm(self, self.request)

    def default_article(self):
        return default_value_from_field(self, self.fields['article'])


class RegionForm(EmbededForm):
    """ Select the memberstate, region, area form
    """

    fields = Fields(interfaces.IStartArticles8910)
    fields['region_subregions'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return MemberStatesForm(self, self.request)

    # def default_region_subregions(self):
    #     return all_values_from_field(self, self.fields['region_subregions'])

    def get_selected_regions_subregions(self):
        return self.data.get('region_subregions')


class MemberStatesForm(EmbededForm):
    fields = Fields(interfaces.IMemberStates)
    fields['member_states'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return AreaTypesForm(self, self.request)

    def get_selected_member_states(self):
        return self.context.data.get('member_states')

    def default_member_states(self):
        return all_values_from_field(self, self.fields['member_states'])

    def get_selected_regions_subregions(self):
        return self.context.data.get('region_subregions')


class AreaTypesForm(EmbededForm):

    fields = Fields(interfaces.IAreaTypes)
    fields['area_types'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        # needed for marine unit ids vocabulary
        self.data['member_states'] = self.context.data['member_states']
        self.data['region_subregions'] = \
            self.context.context.data['region_subregions']

        return MarineUnitIDsForm(self, self.request)

    def get_selected_member_states(self):
        return self.context.data.get('member_states')

    def default_area_types(self):
        # member_states = self.context.data.get('member_states')
        #
        # if member_states:
        #     t = sql.t_MSFD4_GegraphicalAreasID
        #     count, rows = db.get_all_records(
        #         t,
        #         t.c.MemberState.in_(member_states)
        #     )
        #
        #     return [x[2] for x in rows]

        return all_values_from_field(self, self.fields['area_types'])

    def get_available_marine_unit_ids(self):
        return self.subform.get_available_marine_unit_ids()


StartArticle8910View = wrap_form(StartArticle8910Form, MainFormWrapper)


class MarineUnitIDsForm(EmbededForm):
    """ Select the MarineUnitID based on MemberState, Region and Area
    """

    fields = Fields(interfaces.IMarineUnitIDsSelect)
    fields['marine_unit_ids'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        data = self.get_main_form().data
        klass = get_form(data['article'])

        return super(MarineUnitIDsForm, self).get_subform(klass)

    def default_marine_unit_ids(self):
        return all_values_from_field(self.context,
                                     self.fields['marine_unit_ids'])

    def get_available_marine_unit_ids(self):
        marine_unit_ids = self.data.get('marine_unit_ids')

        if marine_unit_ids:
            data = self.data
        else:
            data = {}
            parent = self.context

            # lookup values in the inheritance tree

            for crit in ['area_types', 'member_states', 'region_subregions']:
                data[crit] = getattr(parent, 'get_selected_' + crit)()
                parent = parent.context

        return db.get_marine_unit_ids(**data)


StartArticle11View = wrap_form(StartArticle11Form, MainFormWrapper)
StartArticle1314View = wrap_form(StartArticle1314Form, MainFormWrapper)


class StartArticle89102018Form(MainForm):
    record_title = 'Articles 8, 9, 10'
    name = 'msfd-c4'

    fields = Fields(interfaces.IArticleSelect2018)
    session_name = 'session_2018'

    def get_subform(self):
        article = self.data['article']

        if article:
            if isinstance(article, tuple):
                klass = article[0]
            else:
                klass = article

            return klass(self, self.request)

    def default_article(self):
        return default_value_from_field(self, self.fields['article'])


StartArticle89102018View = wrap_form(StartArticle89102018Form, MainFormWrapper)

# discover and register associated views

scan('a8ac')
scan('a8b')
scan('a9')
scan('a10')
scan('a89102018')
