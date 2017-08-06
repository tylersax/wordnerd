from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Note, FbPost, WOTD, FBUser, LoggedMessage

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

class WOTDSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WOTD
        fields = '__all__'

    def create(self, validated_data):
        return WOTD.objects.create(**validated_data)

class FBUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FBUser
        fields = '__all__'

    def create(self, validated_data):
        return FBUser.objects.create(**validated_data)

class LoggedMessageSerializer(serializers.HyperlinkedModelSerializer):
    recipient = serializers.HyperlinkedIdentityField(view_name='fbuser-detail')
    sender = serializers.HyperlinkedIdentityField(view_name='fbuser-detail')

    class Meta:
        model = LoggedMessage
        fields = '__all__'

    def create(self, validated_data):
        return LoggedMessage.objects.create(**validated_data)
