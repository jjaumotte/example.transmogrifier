.. contents::

Introduction
============

Create package::

  $ bin/templer plone_basic example.transmogrifier

Declare c.transmogrifier as a dependency in setup.py::

      install_requires=[
          'setuptools',
          'collective.transmogrifier',
      ],

If you use ZopeSkel, make sure the depencencies are included (configure.zcml)::

  <configure
    xmlns="http://namespaces.zope.org/zope"
    i18n_domain="example.transmogrifier">

    <includeDependencies package="." />

  </configure>

Run buildout::

  $ bin/buildout

Add transmogrifier pipeline definition with a csv source section and a logger
(src/example/transmogrifier/news.cfg)::

  [transmogrifier]
  pipeline =
      csvsource
      logger

  [csvsource]
  blueprint = collective.transmogrifier.sections.csvsource
  filename = example.transmogrifier:data/news.csv

  [logger]
  blueprint = collective.transmogrifier.sections.logger
  name = logger
  level = INFO

Add CSV file to import from (src/example/transmogrifier/data/news.csv)::

  id,title,description
  news-1, News One, First news item
  news-2, News Two, Second news item

Register transmogrifier pipeline (configure.zcml)::

  <configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:transmogrifier="http://namespaces.plone.org/transmogrifier"
    i18n_domain="collective.transmogrifier">

  <transmogrifier:registerConfig
    name="news-import"
    title="News import pipeline"
    description="Transmogrifier pipeline to import news"
    configuration="news.cfg"
    />

  </configure>

Test transmogrifier pipeline
(src/example/transmogrifier/tests/test_setup.py)::

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

Add import news browser view (src/example/transmogrifier/browser.py)::

  # -*- coding: utf-8 -*-
  from zope.site.hooks import getSite
  from z3c.form import form
  from z3c.form import button
  from collective.transmogrifier.transmogrifier import Transmogrifier


  class ImportForm(form.Form):

      @button.buttonAndHandler(u'Import News')
      def handle_import_news(self, action):
          transmogrifier = Transmogrifier(getSite())
          transmogrifier(u'news-import')

Register browser view (src/example/transmogrifier/configure.zcml)::

  <configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:five="http://namespaces.zope.org/five"
    xmlns:i18n="http://namespaces.zope.org/i18n"
    xmlns:transmogrifier="http://namespaces.plone.org/transmogrifier"
    i18n_domain="example.transmogrifier">

    <includeDependencies package="." />

    <transmogrifier:registerConfig
      name="news-import"
      title="News import pipeline"
      description="Transmogrifier pipeline to import news"
      configuration="news.cfg"
      />

    <browser:page
      name="news-import"
      for="Products.CMFPlone.interfaces.siteroot.IPloneSiteRoot"
      class=".browser.ImportForm"
      permission="zope2.View"
      />

  </configure>

Start instance::

  $ bin/instance fg

Create Plone instance and open your browser::

  http://localhost:8080/Plone/news-import

Clicking on the "Import News"-Button will give you the following output
in the console::

  2014-05-12 13:50:25 INFO logger {'description': ' First news item', 'id': 'news-1', 'title': ' News One'}
  2014-05-12 13:50:25 INFO logger {'description': ' Second news item', 'id': 'news-2', 'title': ' News Two'}

Full Example
------------

plone.app.transmogrifier and transmogrify come with lots of transmogrifier
pipeline steps. To install those packages just add them to your setup.py::

      install_requires=[
          ...
          'transmogrify.dexterity',
          'plone.app.transmogrifier',
      ]

Run buildout to fetch the dependencies::

  $ bin/buildout

An example pipeline that reads objects from a CSV file and creates them as
object in Plone (src/example/transmogrifier/news.cfg)::

  [transmogrifier]
  pipeline =
      csvsource
      content_type
      title_to_id
      generate_path
      disable_versioning
      constructor
      enable_versioning
      schemaupdater
      reindexobject
      logger

  [csvsource]
  blueprint = collective.transmogrifier.sections.csvsource
  filename = example.transmogrifier:data/news.csv

  [content_type]
  blueprint = collective.transmogrifier.sections.inserter
  key = string:_type
  value = string:Document
  condition = python:'_type' not in item

  [title_to_id]
  blueprint = plone.app.transmogrifier.urlnormalizer
  source-key = title
  destination-key = string:_generated_id
  locale = string:en
  condition = python:'_path' not in item

  [generate_path]
  blueprint = collective.transmogrifier.sections.inserter
  key = string:_path
  value = python:(item['_folder'] + '/' if '_folder' in item else '') + item['_generated_id']
  condition = python:'_path' not in item

  [disable_versioning]
  blueprint = plone.app.transmogrifier.versioning.disable

  [constructor]
  blueprint = collective.transmogrifier.sections.constructor
  required = True

  [enable_versioning]
  blueprint = plone.app.transmogrifier.versioning.enable

  [schemaupdater]
  blueprint = transmogrify.dexterity.schemaupdater

  [reindexobject]
  blueprint = plone.app.transmogrifier.reindexobject

  [logger]
  blueprint = collective.transmogrifier.sections.logger
  name = Object created
  level = INFO
