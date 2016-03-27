from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, Group
import logging
#import wit
wit_at = 'EJI7TK2JFPGOJAXNT7I3M5HWAS52ENEM'

import json

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
        topic.setTopic()
        return topic

    def setTopic(self):
        message = self.message
        #wit.init()
        #wit_response = wit.text_query(message, wit_at)
        #intent = json.loads(wit_response)['outcomes'][0]['intent']
        #self.name = intent
        self.name = message

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
