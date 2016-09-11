import requests
import feedparser

def send_message(user, message):
    access_token = 'EAACogSuZCOdYBAMQELrH7CpTvbKqx6ckRvJ6VeyiZA3bqCWCvaZAJ8H3wwWeVKTBSbhvkcnzAWZCZCpvpXSljqyzQrSKUJNuVjRsT4WtYMXZCFMyLSLUzNYJE6btdHxZAZB50w9YN81CjJKkwQEIbgTb6VUVNFoMuZCbaNRJaUQjrMmUPMrIZAwxUR'
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token
    payload = {'recipient':{'id':user},'message':{'text':message}}
    r = requests.post(url, json=payload)
    return r.json()

def get_definition(word):
    key = '988bd8a9-46f8-44b0-ba96-3ab3d55f159e'
    url = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/{word}?key={key}'.format(word=word, key=key)
    xml = feedparser.parse(url)

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
