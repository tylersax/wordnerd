from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Note, FbPost

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class NoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

    def create(self, validated_data):
        return Note.objects.create(**validated_data)

class FbPostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FbPost
        fields = '__all__'

    def create(self, validated_data):
        return FbPost.objects.create(**validated_data)
