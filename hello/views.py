from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, NoteSerializer, FbPostSerializer, WOTDSerializer, FBUserSerializer
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
from .models import Greeting, Note, FbPost, Conversation, WOTD, FBUser

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
        # serializer = FbPostSerializer(data=data)
        # serializer.is_valid()
        # serializer.save()

        psid=data['entry'][0]['messaging'][0]['sender']['id']

        # start by defining the response functionality here and in utils,
        # but this should really be pushed into a 'conversation' object

        if "postback" in data['entry'][0]['messaging'][0]:
            payload = data['entry'][0]['messaging'][0]['postback']['payload']
        elif "quick_reply" in data['entry'][0]['messaging'][0]['message']:
            payload = data['entry'][0]['messaging'][0]['message']['quick_reply']['payload']
        else:
            payload = ''

        if payload and payload != 'null':
            payload_function = payload.split('.')[0]
            payload_param = payload.split('.')[1]

            if payload_function == 'define':
                #this should be in a function
                existing_wotd = WOTD.objects.filter(word=payload_param)
                message = '\"{definition}\"'.format(definition=existing_wotd[0].definition)
                replies = {':thumbs_up_sign:':'0.0',':thumbs_down_sign:':'0.0'}
                utils.send_message_with_replies(psid, message, replies)

            if payload_function == 'get_started':
                profile = utils.get_name_from_psid(psid)
                new_user = FBUser(
                    psid=psid,
                    first_name=profile.get('first_name'),
                    last_name=profile.get('last_name')
                )
                new_user.save()

        # convo = Conversation.create(message_text, user )
        # response = convo.parseMessage(message_text)
        #utils.send_message(user, message_text)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=500)

def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def entry(request):
    return render(request, 'entry.html')
