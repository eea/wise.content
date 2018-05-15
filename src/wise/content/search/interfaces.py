from zope.interface import Attribute, Interface
from zope.schema import Choice, Int, List  # , TextLine


class IEmbededForm(Interface):
    """ A form that is "embeded" in another form
    """

    def extras():
        """ Return extra-html to show after the main data
        """


class IItemDisplayForm(IEmbededForm):
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


class IStartArticles8910(Interface):
    member_states = List(
        title=u"Member state",
        value_type=Choice(vocabulary="wise_search_member_states"),
        required=True,
    )

    region_subregions = List(
        title=u"Region and Subregions",
        value_type=Choice(vocabulary="wise_search_region_subregions"),
        required=True,
    )

    area_types = List(
        title=u"Area Type",
        value_type=Choice(vocabulary="wise_search_area_type"),
        required=True,
    )


class IMarineUnitIDsSelect(Interface):
    marine_unit_ids = List(
        title=u"MarineUnitID",
        description=u"Select one or more MarineUnitIDs that you're interested",
        value_type=Choice(vocabulary="wise_search_marine_unit_ids_vocab")
    )


class IArticleSelect(Interface):
    article = Choice(title=u"Article",
                     required=False,
                     default='',
                     vocabulary="wise_search_articles")


class IMarineUnitIDSelect(Interface):
    marine_unit_id = Choice(
        title=u"MarineUnitID",
        description=u"Select one or more MarineUnitIDs that you're interested",
        vocabulary="wise_search_marine_unit_id_vocab"
    )