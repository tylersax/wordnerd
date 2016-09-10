#!/usr/bin/env python
import utils
import feedparser

wotd_feed = 'http://www.dictionary.com/wordoftheday/wotd.rss'
rss = feedparser.parse(wotd_feed)
wotd = rss.entries[0]['summary'].split(':', 1)[0]

utils.send_message(1046310852095543, 'The word of the day is {wotd}.'.format(wotd=wotd))
