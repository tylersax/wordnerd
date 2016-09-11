#!/usr/bin/env python\

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gettingstarted.settings")
from django.conf import settings

import django
django.setup()

import utils
import feedparser
from hello.models import WOTD

wotd_feed = 'http://www.dictionary.com/wordoftheday/wotd.rss'
rss = feedparser.parse(wotd_feed)
wotd_string = rss.entries[0]['summary'].split(':', 1)[0]

#wotd = WOTD(word=wotd_string)
print wotd_string
utils.send_message(1046310852095543, 'The word of the day is \'{wotd}.\''.format(wotd=wotd_string))
