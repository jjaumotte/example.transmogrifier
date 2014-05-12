from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection
from zope.interface import classProvides
from zope.interface import implements


class AddTypeSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.transmogrifier = transmogrifier
        self.name = name
        self.options = options
        self.previous = previous
        if 'type' in options:
            self.type = options['type']

    def __iter__(self):
        for item in self.previous:
            item['_type'] = self.type
            yield item
