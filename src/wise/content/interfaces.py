# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IWiseContentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

class IWiseContentTypesSettings(Interface):
    """ portal_registry IWiseContentTypes settings
    """

    fullwidthFor = schema.Tuple(
        title=u"Fullwidth ContentTypes",
        description=u"Enable body fullwidth class for the "
                      "following content-types",
        required=False,
        value_type=schema.Choice(
            vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes")
    )