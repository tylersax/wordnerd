#!/usr/bin/env python\

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gettingstarted.settings")
from django.conf import settings

import django
django.setup()

import hello.utils as utils
import feedparser
from hello.models import WOTD, FBUser

wotd_feed = 'http://www.dictionary.com/wordoftheday/wotd.rss'
rss = feedparser.parse(wotd_feed)
wotd_string = rss.entries[0]['summary'].split(':', 1)[0]

existing_wotd = WOTD.objects.filter(word=wotd_string)
if len(existing_wotd) > 1:
    wotd = existing_wotd[0]
else:
    definition = utils.get_definition(wotd_string)
    wotd = WOTD(
        word=wotd_string,
        definition=definition
    )
    wotd.save()

print wotd.word

users = FBUser.objects.all()
for user in users:
    print user.psid
    utils.send_message(user.psid, 'The word of the day is \"{wotd}.\"'.format(wotd=wotd.word))
    utils.send_message(user.psid, 'It means, \"{definition}\"'.format(definition=wotd.definition))
