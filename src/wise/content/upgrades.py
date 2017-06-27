import logging

logger = logging.getLogger('wise.content.migration')
default_profile = 'profile-wise.content:default'


def upgrade_to_2(context):
    logger.info("Upgrading to 2")

    # need to reimport wise.content, it has updated workflow settings
    context.runImportStepFromProfile(default_profile, 'workflow')
