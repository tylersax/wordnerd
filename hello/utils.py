import requests

def send_message(user, message):
    access_token = 'EAACogSuZCOdYBAPXIZAuwSZA2o61T0E270JjdT3uAowBbcZCpfXZCuApbb90EtIfJbZBK05j8gLwVLYczUvPAaWS4lp9Ivfnmd2AhDtPUWfaKXYCQGdwqOMJOZCxh1KZCd7vHvpCn1SRipi1ZCmkXXZAsFS3ZBh39Ly4IkXHM8m1cvXQDD4aus61U8d'
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token
    payload = {'recipient':{'id':user},'message':{'text':message}}
    r = requests.post(url, json=payload)

    return r.json()
