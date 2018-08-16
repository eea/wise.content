from zope.interface import Attribute, Interface
from zope.schema import Choice, Int, List, Text  # , TextLine

from plone.app.textfield import RichText


class IMainForm(Interface):
    """ A marker interface to easily identify main forms
    """


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
        required=False,
    )

    region_subregions = List(
        title=u"Region and Subregions",
        value_type=Choice(vocabulary="wise_search_region_subregions"),
        required=False,
    )

    area_types = List(
        title=u"Area Type",
        value_type=Choice(vocabulary="wise_search_area_type"),
        required=False,
    )


class IMemberStates(Interface):
    member_states = List(
        title=u"Member state",
        value_type=Choice(vocabulary="wise_search_member_states"),
        required=False,
    )


class IStartArticles1314(Interface):
    report_type = Choice(
        title=u"Report Type",
        vocabulary="wise_search_a1314_report_types",
        required=False,
    )

    region = Choice(
        title=u"Region",
        vocabulary="wise_search_a1314_regions",
        required=False,
    )


class IStartArticle11(Interface):
    monitoring_programme_types = List(
        title=u"Monitoring programme Type",
        value_type=Choice(
            vocabulary="wise_search_monitoring_programme_vb_factory"),
        required=False
    )

    monitoring_programme_info_types = Choice(
        title=u"Information Type",
        vocabulary="wise_search_monitoring_programme_info_types",
        required=False
    )


class IMonitoringProgramme(Interface):
    country = List(
        title=u"Country",
        value_type=Choice(vocabulary="wise_search_art11_country"),
        required=False
    )

    region = List(
        title=u"Region",
        value_type=Choice(vocabulary="wise_search_art11_region"),
        required=False
    )

    marine_unit_id = List(
        title=u"Marine Unit IDs",
        value_type=Choice(vocabulary="wise_search_art11_marine_unit_id"),
        required=False
    )


class IMonitoringSubprogramme(Interface):
    country = List(
        title=u"Country",
        value_type=Choice(vocabulary="wise_search_art11_country_ms"),
        required=False
    )

    region = List(
        title=u"Region",
        value_type=Choice(vocabulary="wise_search_art11_region_ms"),
        required=False
    )

    marine_unit_id = List(
        title=u"Marine Unit IDs",
        value_type=Choice(vocabulary="wise_search_art11_marine_unit_id_ms"),
        required=False
    )


class IMarineUnitIDsSelect(Interface):
    marine_unit_ids = List(
        title=u"MarineUnitIDs",
        # description=u"Select one or more MarineUnitIDs that you're
        # interested",
        value_type=Choice(vocabulary="wise_search_marine_unit_ids"),
        required=False
    )


class IArticleSelect(Interface):
    article = Choice(title=u"Article",
                     required=False,
                     default='',
                     vocabulary="wise_search_articles")


class IMarineUnitIDSelect(Interface):
    marine_unit_id = Choice(
        title=u"MarineUnitID",
        # description=u"Select one or more MarineUnitIDs that you're
        # interested",
        required=False,
        vocabulary="wise_search_marine_unit_id"
    )


class IA1314UniqueCodes(Interface):
    unique_codes = List(
        title=u"Unique Codes",
        # description=u"Select one or more Unique Codes that you're
        # interested",
        required=False,
        value_type=Choice(vocabulary="wise_search_a1314_unique_codes")
    )


# Articles 8, 9, 10
# 2018 reporting year
class IArticleSelect2018(Interface):
    article = Choice(title=u"Article",
                     required=False,
                     default='',
                     vocabulary="wise_search_articles_2018")


class ICountryCodeMarineReportingUnits(Interface):
    country_code = List(
        title=u"Country Code",
        required=False,
        value_type=Choice(vocabulary="wise_search_a2018_country")
    )

    marine_reporting_unit = List(
        title=u"Marine Reporting Unit",
        required=False,
        value_type=Choice(vocabulary="wise_search_a2018_marine_reporting_unit")
    )


class ICountryCode(Interface):
    country_code = List(
        title=u"Country Code",
        required=False,
        value_type=Choice(vocabulary="wise_search_a2018_country")
    )


class ICountryCodeGESComponents(Interface):
    country_code = List(
        title=u"Country Code",
        required=False,
        value_type=Choice(vocabulary="wise_search_a2018_country")
    )

    ges_component = List(
        title=u"GES Component",
        required=False,
        value_type=Choice(vocabulary="wise_search_a2018_ges_component_art9")
    )


class IFeaturesGESComponents(Interface):
    feature = List(
        title=u"Features",
        required=False,
        value_type=Choice(vocabulary="wise_search_a2018_feature")
    )

    ges_component = List(
        title=u"GES Component",
        required=False,
        value_type=Choice(vocabulary="wise_search_a2018_ges_component")
    )


class IFeatures(Interface):
    feature = List(
        title=u"Features",
        required=False,
        value_type=Choice(vocabulary="wise_search_a2018_feature_art9")
    )


class IFeatures81c(Interface):
    feature = List(
        title=u"Features",
        required=False,
        value_type=Choice(vocabulary="wise_search_a2018_feature_art81c")
    )


class IIndicatorsGESFeatureMRU(Interface):
    ges_component = List(
        title=u"GES Component",
        required=False,
        value_type=Choice(vocabulary="wise_search_a2018_ges_component_ind")
    )

    feature = List(
        title=u"Features",
        required=False,
        value_type=Choice(vocabulary="wise_search_a2018_feature_ind")
    )

    marine_reporting_unit = List(
        title=u"Marine Reporting Unit",
        required=False,
        value_type=Choice(vocabulary="wise_search_a2018_mru_ind")
    )


class IComplianceModule(Interface):
    file = Choice(
        title=u"File",
        required=False,
        vocabulary="wise_search_compliance_factory"
    )


class IComplianceAssessment(Interface):
    com_assessment = Text(
        title=u"COM assessments",
        required=False,
    )

    assessment_comment = Text(
        title=u"Assessments comments",
        required=False
    )
