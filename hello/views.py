from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, NoteSerializer, FbPostSerializer, WOTDSerializer, FBUserSerializer, LoggedMessageSerializer
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.six import BytesIO
import logging
from rest_framework.parsers import JSONParser
import utils
from .models import Greeting, Note, FbPost, Conversation, WOTD, FBUser, LoggedMessage
import datetime
import time

class FBUserViewSet(viewsets.ModelViewSet):

    queryset = FBUser.objects.all()
    serializer_class = FBUserSerializer

class WOTDViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows WOTD to be viewed or edited.
    """
    queryset = WOTD.objects.all()
    serializer_class = WOTDSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows notes to be viewed or edited.
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class FbPostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows notes to be viewed or edited.
    """
    queryset = FbPost.objects.all()
    serializer_class = FbPostSerializer

class LoggedMessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows notes to be viewed or edited.
    """
    queryset = LoggedMessage.objects.all()
    serializer_class = LoggedMessageSerializer


@api_view(['GET'])
def returnString(request):
    # if request.method == 'GET':
    #     notes = Note.objects.all()
    #     serializer = NoteSerializer(notes, context=request, many=True)
    #     return Response(serializer.data)

    return JsonResponse({'foo':str(request.GET.lists())})

@api_view(['GET','POST'])
@permission_classes((AllowAny,))
def webhook(request):

    myVerifyToken = '897698241086'
    if request.method =='GET' and str(request.GET.get('hub.verify_token')) == myVerifyToken:
        return HttpResponse(str(request.GET.get('hub.challenge')),status=200)
    elif request.method =='POST':
        logging.debug(request.body)
        print(request.body)
        stream = BytesIO(str(request.body))
        data = JSONParser().parse(stream)

        log = LoggedMessage()

        message = data['entry'][0]['messaging'][0].get('message')

        psid=data['entry'][0]['messaging'][0]['sender']['id']

        # Look up the sender. Create a new FBUser if none exists
        sender_query = FBUser.objects.filter(psid=psid)
        if sender_query.count()==0:
            profile = utils.get_name_from_psid(psid)
            sender = FBUser(
                psid=psid,
                first_name = profile.get('first_name'),
                last_name = profile.get('last_name')
            )
            sender.save()
        else:
            sender = sender_query[0]
        log.sender=sender

        recipient = FBUser.objects.filter(psid=219247181443199)
        log.recipient=recipient[0]
        message_text = ''

        if message:
            log.mid=message.get('mid')
            if 'text' in message:
                log.text = message.get('text')
                message_text = message.get('text')
            if 'attachments' in message:
                log.attachment_url=message.get('attachments')[0]['payload']['url']
        else:
            log.mid='get_started_' + str(time.time())

        timestamp = data['entry'][0]['messaging'][0]['timestamp']
        log.timestamp_sent=datetime.datetime.fromtimestamp(timestamp/1000)


        # start by defining the response functionality here and in utils,
        # but this should really be pushed into a 'conversation' object

        if "postback" in data['entry'][0]['messaging'][0]:
            payload = data['entry'][0]['messaging'][0]['postback']['payload']
            log.message_type='received'
        elif "read" in data['entry'][0]['messaging'][0]:
            # this is just a read receipt, do nothing for now
            log.message_type='read'
            payload='null'
        elif "quick_reply" in data['entry'][0]['messaging'][0]['message']:
            payload = data['entry'][0]['messaging'][0]['message']['quick_reply']['payload']
            log.message_type='received'
        else:
            payload = ''
            log.message_type='received'

        log.payload=payload
        log.save()


        if payload and payload != 'null':
            payload_function = payload.split('.')[0]
            payload_param = payload.split('.')[1]

            if payload_function == 'define':
                #this should be in a function
                existing_wotd = WOTD.objects.filter(word=payload_param)
                response = '{definition}'.format(definition=existing_wotd[0].definition)
                replies = {':thumbs_up_sign:':'reply.yes',':thumbs_down_sign:':'reply.no'}
                utils.send_message_with_replies(psid, response, replies)

            if payload_function == 'get_started':
                greeting = """
                Hey there, {first_name}. Let\'s learn some words, shall we? If it\'s alright with you, I\'ll message you every morning with a new word of the day.
                """.format(first_name=sender.first_name)

                replies = {
                    ':thumbs_up_sign: Let\'s do it!':'subscribe.yes',
                    ':thumbs_down_sign: No thanks.':'subscribe.no'
                    }

                utils.send_message_with_replies(psid, greeting, replies)

            if payload_function == 'subscribe':
                if payload_param == 'yes':
                    reply = 'That\'s what I wanted to hear :raised_hands: You\'ll get your first word tomorrow. See you then!'
                    sender.subscribed = True
                    sender.save()

                else:
                    reply = 'It\'s cool - I get it. :no_good:'

                utils.send_message(psid, reply)


        if message_text.split(' ', 1)[0].lower() == 'define':
             lookup = message_text.split(' ', 1)[1].lower()
             definition = utils.get_definition(lookup)
             replies = {':thumbs_up_sign:':'reply.yes',':thumbs_down_sign:':'reply.no'}
             utils.send_message_with_replies(psid, definition, replies)

        # convo = Conversation.create(message_text, user )
        # response = convo.parseMessage(message_text)
        #utils.send_message(user, message_text)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=500)

def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def privacypolicy(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'privacypolicy.html')

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def entry(request):
    return render(request, 'entry.html')
