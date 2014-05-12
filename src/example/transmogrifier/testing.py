from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class ExampletransmogrifierLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import example.transmogrifier
        xmlconfig.file(
            'configure.zcml',
            example.transmogrifier,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')


EXAMPLE_TRANSMOGRIFIER_FIXTURE = ExampletransmogrifierLayer()
EXAMPLE_TRANSMOGRIFIER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EXAMPLE_TRANSMOGRIFIER_FIXTURE,),
    name="ExampletransmogrifierLayer:Integration"
)
EXAMPLE_TRANSMOGRIFIER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EXAMPLE_TRANSMOGRIFIER_FIXTURE, z2.ZSERVER_FIXTURE),
    name="ExampletransmogrifierLayer:Functional"
)
