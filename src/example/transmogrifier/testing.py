from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class ExampletransmogrifierLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import example.transmogrifier
        xmlconfig.file(
            'configure.zcml',
            example.transmogrifier,
            context=configurationContext
        )


EXAMPLE_TRANSMOGRIFIER_FIXTURE = ExampletransmogrifierLayer()
EXAMPLE_TRANSMOGRIFIER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EXAMPLE_TRANSMOGRIFIER_FIXTURE,),
    name="ExampletransmogrifierLayer:Integration"
)
EXAMPLE_TRANSMOGRIFIER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EXAMPLE_TRANSMOGRIFIER_FIXTURE, z2.ZSERVER_FIXTURE),
    name="ExampletransmogrifierLayer:Functional"
)
