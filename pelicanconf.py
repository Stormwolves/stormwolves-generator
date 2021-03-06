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
from stormwolves.plugins.photos import photos


PLUGINS = [pages, articles, page_hierarchy, tipue_search, photos]

COPYRIGHT_LABEL = "&copy; {0} Stormwolves".format(datetime.datetime.now().year)

AUTHOR = u'Test'
SITENAME = u'Stormwolves Team'
SITE_SLOGAN = u''
SITEURL = ''
THEME = 'stormwolves-theme'
PATH = 'content'
MENUITEMS = (('Archives', '/archives.html'),)

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = u'en'

# Photos/Galleries
PHOTO_LIBRARY = "content/news/media"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
DISPLAY_PAGES_ON_MENU = True

ARTICLE_PATHS = ['news']
ARTICLE_SAVE_AS = 'news/{slug}.html'
ARTICLE_PICTURES = 'images'  # Relative to the ARTICLE_PATHS
ARTICLE_DEFAULT_PICTURE = '__default_article_image.jpg'
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
DIRECT_TEMPLATES = ['index', 'tags', 'categories', 'authors', 'archives', 'search', 'team']

SCANNER = Scanner("content")
SCANNER.articles_paths = ARTICLE_PATHS
SCANNER.scan()