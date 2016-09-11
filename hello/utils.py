import requests

def send_message(user, message):
    access_token = 'EAACogSuZCOdYBADiCAmynpIKjpBXTi0fL9aEiecBIFsh8OWqnbi3rfbW9nle1HSA9QFAGQWsytVLMGARGg3gz0MNx3Cu8tlWBlt059m4jG3kmWe5eleqxbxBqb9dju7whQnWCvbKa6QiyBAcZBFxr2IOHDKwqLYHLS4WOmZCAZDZD'
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token
    payload = {'recipient':{'id':user},'message':{'text':message}}
    r = requests.post(url, json=payload)
    print r.json()
    print r.url
    return r.json()
