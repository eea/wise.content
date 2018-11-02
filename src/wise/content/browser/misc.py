# -*- coding: utf-8 -*-

import json
import requests
from OFS.ObjectManager import BeforeDeleteException
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import getToolByName
from Products.Five.browser import BrowserView
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.iterate.interfaces import ICheckinCheckoutPolicy
from plone.api import portal
from plone.fieldsets.fieldsets import FormFieldsets
from redminelib import Redmine
from requests.auth import HTTPDigestAuth
from wise.content import _
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.interface import Interface, implements
from zope.schema import TextLine
# from plone.memoize.view import memoize
# from plone.registry.interfaces import IRegistry
# from zope.component import getUtility
from BTrees.OOBTree import OOBTree
import chardet
import transaction

ANNOTATION_KEY = 'translation.msfd.storage'


class SendTranslationRequest(BrowserView):
    """ Sends translation request
    """

    def __call__(self):
        if self.request.form.get('id', None):
            return self.get_translation_from_annot()
        text = self.request.form.get('text-to-translate', '')
        targetLanguages = self.request.form.get('targetLanguages', ['EN'])
        sourceLanguage = self.request.form.get('sourceLanguage', '')
        externalReference = self.request.form.get('externalReference', '')
        # sourceObjectLocation = self.request.form.get('sourceObject', '')
        data = {
            'priority': 5,
            'callerInformation': {
                'application': 'Marine_EEA_20180706',
                'username': 'ipetchesi',
            },
            'domain': 'SPD',
            'externalReference': externalReference,
            'textToTranslate': text,
            'sourceLanguage': sourceLanguage,
            'targetLanguages': targetLanguages,
            'destinations': {
                'httpDestinations':
                    ['http://office.pixelblaster.ro:3880/Plone/marine/translation-callback/'],
                'emailDestinations':
                    ['iulian.petchesi@eaudeweb.ro']
                    }
        }

        dataj = json.dumps(data)
        headers = {'Content-Type': 'application/json'}

        service_url = 'https://webgate.ec.europa.eu/etranslation/si/translate'
        result = requests.post(service_url, auth=HTTPDigestAuth(
                 'Marine_EEA_20180706', ''),
                 data=dataj, headers=headers)

        self.request.response.headers.update(headers)
        res = {
            "transId": result.content,
            "externalRefId": externalReference
        }
        return json.dumps(res)

    def get_translation_from_annot(self):
        key = self.request.form.get('key', '')
        site = self.context.Plone
        annot = IAnnotations(site, None)
        if annot:
            translation = annot[ANNOTATION_KEY].get(key, None)
            if translation:
                # try:
                    return translation
                # except:
                    # import pdb; pdb.set_trace()


class TranslationCallback(BrowserView):
    """ Saves the translation in Annotations
    """

    def __call__(self):
        self.saveToAnnotation()
        return self.request.form

    def saveToAnnotation(self):
        site = portal.getSite()
        annot = IAnnotations(site, None)
        if ANNOTATION_KEY not in annot.keys():
            annot[ANNOTATION_KEY] = OOBTree()

        # transId = self.request.form.get('request-id', '')
        # targetLang = self.request.form.get('target-language', '')
        originalText = self.request.form.get('external-reference')

        self.request.form.pop('request-id')
        self.request.form.pop('target-language')
        self.request.form.pop('external-reference')

        translatedText = self.request.form.keys()[0]

        encoding = chardet.detect(translatedText)['encoding']
        # import pdb; pdb.set_trace()
        translatedText = translatedText.decode(encoding)
        trans_entry = {originalText: translatedText}
        annot[ANNOTATION_KEY].update(trans_entry)
        transaction.commit()


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


class IssueCreate(BrowserView):
    """
    The view is called via the custom script adapter in the pfg form
    It then creates tickets in the redmine project

    How to get tracker ids:

    >>> trackers = redmine.tracker.all()
    >>> trackers[index].id

    Getting categories:

    >>> redmine.issue_category.filter(project_id='project_id')[index].id

    Getting issue statuses:

    >>> redmine.issue_status.all()[index].id

    Getting all projects:

    >>> projects = redmine.project.all(offset=10, limit=100)
    >>> projects
    <redminelib.resultsets.ResourceSet object with Project resources>

    More here:
    https://python-redmine.com/resources/issue.html

    """

    def __call__(self, REQUEST):
        portal_properties = getToolByName(self.context, 'portal_properties')
        redmine_properties = portal_properties.redmine_configuration_properties

        redmine_url = redmine_properties.redmine_url.encode()
        version = redmine_properties.version
        user_key = redmine_properties.user_api_key.encode()
        project = redmine_properties.project.encode()

        redm = Redmine(redmine_url, key=user_key, version=version)

        subject = REQUEST.form.get('topic', 'generic title')
        comments = REQUEST.form.get('comments', 'description')
        issue_from = REQUEST.form.get('replyto', 'generic title')
        description = comments + "\n From: " + issue_from

        redm.issue.create(
            project_id=project,  # required
            subject=subject,  # required
            description=description,
            tracker_id=4,
            status_id=1,
            category_id=794,
        )
