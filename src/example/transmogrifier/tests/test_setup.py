# -*- coding: utf-8 -*-
from zope.site.hooks import getSite
from collective.transmogrifier.transmogrifier import Transmogrifier

from example.transmogrifier.testing import \
  EXAMPLE_TRANSMOGRIFIER_INTEGRATION_TESTING
import unittest2 as unittest


class TestExample(unittest.TestCase):

  layer = EXAMPLE_TRANSMOGRIFIER_INTEGRATION_TESTING

  def setUp(self):
      self.transmogrifier = Transmogrifier(getSite())

  def test_news_import_transmogrifier(self):
      self.transmogrifier(u'news-import')