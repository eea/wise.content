from OFS.ObjectManager import BeforeDeleteException
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import getToolByName
from Products.Five.browser import BrowserView
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.iterate.interfaces import ICheckinCheckoutPolicy
from plone.fieldsets.fieldsets import FormFieldsets
from wise.content import _
from zope.component import adapts
from zope.interface import Interface, implements
from zope.schema import TextLine


class FixCheckout(BrowserView):
    """ A view to fix getBaseline error when the original item was deleted
    and only the copy remains.
    """
    def __call__(self):
        policy = ICheckinCheckoutPolicy(self.context, None)
        relation = policy._get_relation_to_baseline()
        relation.from_object = relation.to_object
        relation._p_changed = True
        return "Fixed"


def preventFolderDeletionEvent(object, event):
    for obj in object.listFolderContents():
        iterate_control = obj.restrictedTraverse('@@iterate_control')
        if iterate_control.is_checkout():
            # Cancel deletion
            raise BeforeDeleteException


class IRedmineSchema(Interface):
    """ Redmine configuration schema """

    redmine_url = TextLine(
        title=_(u'Enter redmine url:'),
        default=_(u''),
        description=_(u''),
        required=True,
    )

    version = TextLine(
        title=_(u'Enter the redmine version: (OPTIONAL)'),
        default=_(u''),
        required=False,
    )

    user_api_key = TextLine(
        title=_(u'Enter the user api key which has access to your project.'),
        default=_(u''),
        description=_(u"The API key can be found on users account page when "
                      u"logged in, on the right-hand pane of the default "
                      u"layout."),
        required=True,
    )

    project = TextLine(
        title=_(u'Enter the project id/name.'),
        default=_(u''),
        required=True,
    )


class BaseControlPanelAdapter(SchemaAdapterBase):
    """ Base control panel adapter """

    def __init__(self, context):
        super(BaseControlPanelAdapter, self).__init__(context)
        portal_properties = getToolByName(context, 'portal_properties')
        self.context = portal_properties.redmine_configuration_properties


class RedmineControlPanelAdapter(BaseControlPanelAdapter):
    """ Redmine settings control panel adapter """
    adapts(IPloneSiteRoot)
    implements(IRedmineSchema)

    redmine_url = ProxyFieldProperty(IRedmineSchema['redmine_url'])
    version = ProxyFieldProperty(IRedmineSchema['version'])
    user_api_key = ProxyFieldProperty(IRedmineSchema['user_api_key'])
    project = ProxyFieldProperty(IRedmineSchema['project'])


baseset = FormFieldsets(IRedmineSchema)
baseset.id = 'redmine-configuration'
baseset.label = _(u'Redmine configuration')


class RedmineControlPanel(ControlPanelForm):
    """ """
    form_fields = FormFieldsets(baseset)

    label = _('Redmine settings')
    description = _("Configure settings for redmine. This is used in a "
                    "ploneformgen form for the purpose of creating issues in "
                    "projects.")
    form_name = _('Redmine Settings')
