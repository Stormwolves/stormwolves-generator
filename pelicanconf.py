#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import datetime
import os
import sys
sys.path.append(os.path.abspath("."))

from stormwolves.scanner import Scanner
from stormwolves.plugins.pages import pages
from stormwolves.plugins.articles import articles
from stormwolves.plugins.tipuesearch import tipue_search
from stormwolves.plugins.pagehierarchy import page_hierarchy

PLUGINS = [pages, articles, tipue_search, page_hierarchy]
SCANNER = Scanner("content").scan()
COPYRIGHT_LABEL = "&copy; {0} Stormwolves".format(datetime.datetime.now().year)

AUTHOR = u'Test'
SITENAME = u'Stormwolves Team'
SITEURL = ''
THEME = 'stormwolves-theme'
PATH = 'content'
MENUITEMS = (('Archives', '/archives.html'),)

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
DISPLAY_PAGES_ON_MENU = True

ARTICLE_PATHS = ['news']
ARTICLE_SAVE_AS = 'news/{slug}.html'
# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 3
PAGINATED_DIRECT_TEMPLATES = ['index', 'archives']
DIRECT_TEMPLATES = ['index', 'tags', 'categories', 'authors', 'archives', 'search']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
