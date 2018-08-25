#!/usr/bin/env python\

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gettingstarted.settings")
from django.conf import settings

import django
django.setup()

import hello.utils as utils
import feedparser
from hello.models import WOTD, FBUser

import datetime

wotd_feed = 'https://wordsmith.org/awad/rss1.xml'
rss = feedparser.parse(wotd_feed)
wotd_string = rss.entries[0]['title']

existing_wotd = WOTD.objects.filter(word=wotd_string)

if len(existing_wotd) > 1:
    wotd = existing_wotd[0]
else:
    # note: there is a utils function to get definition from an API
    # if you ever need that
    definition = rss.entries[0]['summary']
    wotd = WOTD(
        word=wotd_string,
        definition=definition
    )
    wotd.save()

# This hours adjustment will be wrong when daylight savings changes
# Note that weekday() returns Mon-Sun as [0,6]
pst_day_of_week = (datetime.datetime.now() - datetime.timedelta(hours=7)).weekday()

# Only message users on weekdays
if pst_day_of_week not in (5,6):
    users = FBUser.objects.filter(subscribed=True)
    for user in users:
        message = 'The word of the day is \"{wotd}.\"'.format(wotd=wotd.word)
        replies = {'Definition, please?':'define.{wotd}'.format(wotd=wotd.word)}
        utils.send_message_with_replies(user.psid, message, replies)
