from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.interfaces import ISection
from zope.interface import classProvides
from zope.interface import implements

from collective.transmogrifier.utils import Expression, Condition


class ImportUrbanSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.key = Expression(options['key'], transmogrifier, name, options)
        self.value = Expression(options['value'], transmogrifier, name,
                                options)
        self.condition = Condition(options.get('condition', 'python:True'),
                                   transmogrifier, name, options)
        self.previous = previous

    def __iter__(self):
        for item in self.previous:
            key = self.key(item)
            # import ipdb;
            # ipdb.set_trace()
            if item['GENRE'] is not None:
                item['_path'] = item['GENRE']
            if self.condition(item, key=key):
                import ipdb; ipdb.set_trace()
                item[key] = self.value(item, key=key)
            yield item
