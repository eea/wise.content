from zope.interface import Attribute, Interface
from zope.schema import Choice, Int  # , TextLine

from .vocabulary import SubFormsVocabulary


class ISubForm(Interface):
    """ A form that is "embeded" in another form
    """

    def extras():
        """ Return extra-html to show after the main data
        """


class IItemDisplayForm(ISubForm):
    data_template = Attribute(u"Template to be used to show item data")
    extra_data_template = Attribute(u"Template for any extra item data")

    def set_item():
        """ Called from update() to set self.item
        """

    def get_db_results():
        """ Actual DB query implementation to get item
        """

    def get_extra_data():
        """ Return extra data as HTML for this item
        """


class IRecordSelect(Interface):
    """ We use a pagination based record selection
    """

    page = Int(title=u'Record page', required=False, default=0)


class IMain_Articles8910(Interface):

    member_state = Choice(title=u"Member state",
                          required=False,
                          default='',
                          vocabulary="wise_search_member_states")

    region_subregion = Choice(title=u"Region and Subregions",
                              required=False,
                              default='',
                              vocabulary="wise_search_region_subregions")

    area_type = Choice(title=u"Area Type",
                       required=False,
                       default='',
                       vocabulary="wise_search_area_type")


class IArticleSelect(Interface):
    article = Choice(title=u"Select article",
                     required=False,
                     default='',
                     vocabulary="wise_search_articles")


class IMarineUnitIDSelect(Interface):
    marine_unit_id = Choice(title=u"Select MarineUnitID",
                            required=False,
                            default='',
                            vocabulary="wise_search_marine_unit_id_vocab")


# class IA81aSubformSelect(Interface):
#     theme = Choice(title=u"Select theme",
#                    required=False,
#                    vocabulary=SubFormsVocabulary(form))

# wise_search_81a_themes"
# class IA81bSubformSelect(Interface):
#     theme = Choice(title=u"Select theme",
#                    required=False,
#                    default='',
#                    vocabulary="wise_search_81b_themes")
