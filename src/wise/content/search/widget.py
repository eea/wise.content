from zope.component import adapter
from zope.interface import Interface, implementer

from z3c.form.browser.select import SelectWidget
from z3c.form.interfaces import NO_VALUE, IFieldWidget, IFormLayer
from z3c.form.widget import FieldWidget


class MarineUnitIDSelectWidget(SelectWidget):
    """ Special marine widget that, if there's no selection already made,
    always returns at least one value from its possible choices.
    """

    def isSelected(self, term):
        return term.token in self.value

    def extract(self, default=None):
        self.value = []
        value = super(MarineUnitIDSelectWidget, self).extract()

        if value is NO_VALUE:
            # import pdb; pdb.set_trace()
            available = [x['value'] for x in self.items()]

            if available:
                return available[:1]

        return value


def MarineUnitIDSelectFieldWidget(field, source, request=None):

    if request is None:
        real_request = source
    else:
        real_request = request

    return FieldWidget(field, MarineUnitIDSelectWidget(real_request))
