from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, NoteSerializer, FbPostSerializer
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.six import BytesIO
import logging

from .models import Greeting, Note, FbPost

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
        # logging.debug(request.POST.urlencode())
        # print(request.META)
        # serializer = FbPostSerializer(data=request.POST)
        # serializer.is_valid()
        # serializer.save()
        return HttpResponse(str(request.body),status=200)
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
