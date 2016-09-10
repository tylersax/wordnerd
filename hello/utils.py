import requests

def send_message(user, message):
    access_token = 'EAACogSuZCOdYBALENLieXqNBVAgPZCnn7D1F0uviGbTVJTiyPggBqRyszb70aZBSykUFZCJzfNkGsRgplxudzisBQxiUP6D0f6NZC8zQj6FPFDY9pQZC9ni4KcRjMaGghvUgEBFhZC3fnWg1iMWW05rtjeDrif9ZBgMBZCYjfNQZBp8gZDZD'
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + access_token
    payload = {'recipient':{'id':user},'message':{'text':message}}
    r = requests.post(url, json=payload)

    return r.json()
