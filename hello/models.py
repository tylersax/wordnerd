from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, Group
import logging
import urllib
# import pycurl
import utils
from io import BytesIO
wit_at = 'EJI7TK2JFPGOJAXNT7I3M5HWAS52ENEM'

import json
from datetime import datetime

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Note(models.Model):
    # def __init__(self, content, created=None):
    #     #TODO add 'creator' field
    #     self.content = content
    #     self.created = created or datetime.now()
    content = models.TextField(null=True)
    created = models.DateTimeField(default=datetime.now())


    def create(self, validated_data):
        return Note.objects.create(**validated_data)

class FbPost(models.Model):
    object=models.CharField(max_length=100)
    entry=models.TextField()

    def create(self, validated_data):
        return FbPost.objects.create(**validated_data)

class Topic(models.Model):
    # maybe this should actually be an interface, and any new
    # functionality inherits it;s structure
    name=models.CharField(max_length=200)

    # the text string used to trigger the topic
    message=models.TextField()

    # move the topic search here. the topic will ingest the
    # incoming message then instantiate itself as one of several
    # types. More complext logic can be outsourced later.

    @classmethod
    def create(cls, first_message):
        topic = cls(message=first_message)
        #topic.setTopic()
        return topic


    # havingn trouble with pycurl so commenting out for now
    # def setTopic(self):
    #     message = self.message
    #     buffer = BytesIO()
    #     c = pycurl.Curl()
    #     c.setopt(
    #         c.URL,
    #         'https://api.wit.ai/message?v=20141022&q=' + urllib.pathname2url(message)
    #     )
    #     c.setopt(c.WRITEFUNCTION, buffer.write)
    #     c.setopt(c.HTTPHEADER, ['Authorization: Bearer ' + wit_at])
    #     c.perform()
    #     c.close()
    #     intent = json.loads(buffer.getvalue())['outcomes'][0]['intent']
    #     self.name = intent

    def respond(self):
        if self.name == 'helloworld':
            return 'Hello world!'
        elif self.name == 'tutorial':
            return 'Welcome! Let\'s get to know one another.'
        elif self.name =='check_time':
            return 'Sorry, I don\'t know what time it is'
        elif self.name=='math':
            return 'Math response'
        else:
            return 'Sorry, I don\'t understand ' + self.name

class Conversation(models.Model):
    start=models.DateTimeField()
    updated=models.DateTimeField()
    user=models.BigIntegerField()
    state=models.CharField(max_length=200)
    topic=models.OneToOneField(Topic)

    @classmethod
    def create(cls, first_message, user):
        topic = Topic.create(first_message)
        convo = cls(user=user, state='initialized', topic=topic)
        return convo

    def respond(self):
        # call send api for this.user with response
        return self.topic.respond()

    def parseMessage(self, message):
        # send message to this.topic, respond with response, default if no
        # response
        return self.respond()

class WOTD(models.Model):
    word=models.CharField(max_length=100)
    day=models.DateField(default=datetime.now())
    definition=models.TextField()

    def create(self, validated_data):
        return WOTD.objects.create(**validated_data)

class FBUser(models.Model):
    psid=models.CharField(max_length=200)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)

    def create(self, validated_data):
        return FBUser.objects.create(**validated_data)

class LoggedMessage(models.Model):
    LOGGED_MESSAGE_TYPES = (
            ('sent', 'sent'),
            ('recieved', 'recieved'),
            ('read', 'read'),
            ('delivered', 'delivered'),
            ('null', 'null')
     )

    mid=models.CharField(primary_key=True, max_length=100)
    sender=models.ForeignKey(FBUser)
    recipient=models.ForeignKey(FBUser)
    timestamp_logged=models.DateTimeField(auto_now=False)
    timestamp_sent=models.DateTimeField()
    message_type=models.CharField(
        max_length=20,
        choices=LOGGED_MESSAGE_TYPES,
        default='null'
    )
    api_id=models.BigIntegerField()
    payload=models.CharField(max_length=50, blank=True)
    text=models.TextField(blank=True)
    attachment_urls=models.ArrayField(
        models.URLField(),
        size=8,
        blank=True
    )
    extra=models.TextField(blank=True)

    def create(self, validated_data):
        return LoggedMessage.objects.create(**validated_data)
