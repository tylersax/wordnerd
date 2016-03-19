from django.db import models
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
