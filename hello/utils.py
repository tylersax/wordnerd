import requests
import feedparser
from wordnik import *
import json
import emoji

def send_message(user, message):
    start_typing(user)
    access_token = 'EAACogSuZCOdYBAMQELrH7CpTvbKqx6ckRvJ6VeyiZA3bqCWCvaZAJ8H3wwWeVKTBSbhvkcnzAWZCZCpvpXSljqyzQrSKUJNuVjRsT4WtYMXZCFMyLSLUzNYJE6btdHxZAZB50w9YN81CjJKkwQEIbgTb6VUVNFoMuZCbaNRJaUQjrMmUPMrIZAwxUR'
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token
    message_text = emoji.emojize(message)
    payload = {'recipient':{'id':user},'message':{'text':message_text}}
    r = requests.post(url, json=payload)
    return r.json()

def send_message_with_replies(user, message, replies):
    access_token = 'EAACogSuZCOdYBAMQELrH7CpTvbKqx6ckRvJ6VeyiZA3bqCWCvaZAJ8H3wwWeVKTBSbhvkcnzAWZCZCpvpXSljqyzQrSKUJNuVjRsT4WtYMXZCFMyLSLUzNYJE6btdHxZAZB50w9YN81CjJKkwQEIbgTb6VUVNFoMuZCbaNRJaUQjrMmUPMrIZAwxUR'
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token
    replies_json = make_replies_json(replies)
    message_text = emoji.emojize(message)
    payload = {'recipient':{'id':user},'message':{'text':message_text,'quick_replies':replies_json}}
    r = requests.post(url, json=payload)
    return r.json()

def get_name_from_psid(user):
    access_token = 'EAACogSuZCOdYBAMQELrH7CpTvbKqx6ckRvJ6VeyiZA3bqCWCvaZAJ8H3wwWeVKTBSbhvkcnzAWZCZCpvpXSljqyzQrSKUJNuVjRsT4WtYMXZCFMyLSLUzNYJE6btdHxZAZB50w9YN81CjJKkwQEIbgTb6VUVNFoMuZCbaNRJaUQjrMmUPMrIZAwxUR'
    url = 'https://graph.facebook.com/v2.6/'+ user +'?fields=first_name,last_name&access_token=' + access_token
    r = requests.get(url)
    return r.json()

def make_replies_json(replies):
    replies_json = []
    for reply, payload in replies.items():
        reply_text = emoji.emojize(reply)
        reply_json = {"content_type":"text","title":reply_text,"payload":payload}
        replies_json.append(reply_json)

    return json.dumps(replies_json)

def start_typing(user):
    access_token = 'EAACogSuZCOdYBAMQELrH7CpTvbKqx6ckRvJ6VeyiZA3bqCWCvaZAJ8H3wwWeVKTBSbhvkcnzAWZCZCpvpXSljqyzQrSKUJNuVjRsT4WtYMXZCFMyLSLUzNYJE6btdHxZAZB50w9YN81CjJKkwQEIbgTb6VUVNFoMuZCbaNRJaUQjrMmUPMrIZAwxUR'
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token
    payload = {'recipient':{'id':user},'sender_action':'typing_on'}
    r = requests.post(url, json=payload)
    return r.json()

def get_definition(word):
    key = 'be629e6642b73b9c3b4710360ec0a0d680d43628b4ba9e162'
    url = 'http://api.wordnik.com/v4'
    client = swagger.ApiClient(key, url)
    wordApi = WordApi.WordApi(client)
    definitions = wordApi.getDefinitions(word)
    return definitions[0].text

def get_definition_deprecated(word):
    mashape_key = 'iTTnvuGbZymshZqKjqM5mA4XmlLMp13gdUHjsnm0tGZL8JUziQ'
    mashape_url = 'https://wordsapiv1.p.mashape.com/words/{word}'.format(word=word)
    mashape_headers = {
        "X-Mashape-Key": mashape_key,
        "Accept": "application/json"
    }
    r = requests.get(mashape_url, headers=mashape_headers)
    print r.json()
    return r.json()['results'][0]['definition']
