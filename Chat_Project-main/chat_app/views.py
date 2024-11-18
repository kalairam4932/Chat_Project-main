from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat
from django.views.decorators.csrf import csrf_protect
from rest_framework import generics
from rest_framework.response import Response

import os
from datetime import datetime

from chat_project.settings import IMAGE_URL
from .forms import LoginForm, RegistrationForm, RoomForm
from .models import UserAccount, Message, Conversations
from .serializers import UserIdSerializer
# Create your views here.

def login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = UserAccount.objects.filter(username = username, password = password)
            if user:
                request.session['user'] = user.values().first()
                return redirect('home')
            messages.error(request, 'Invalid Credentials')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'loginform': form, 'image_url': os.path.join(IMAGE_URL, 'login.jpeg')})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'{username} Created!')
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', { 'registerform': form, 'image_url': os.path.join(IMAGE_URL, 'login.jpeg') })


def chat_home(request):
    conversations = Conversations.objects.filter(mainuser_id = request.session['user']['id']).values('conv_id', secName = F('seconduser__firstname'), secId = F('seconduser__id'),secProfile = Concat(Value(IMAGE_URL), 'seconduser__profile_pic', output_field = CharField()))
    excluded_users = [conv['secId'] for conv in conversations]
    excluded_users.append(request.session['user']['id'])
    avail_users = UserAccount.objects.exclude(id__in = excluded_users).values('id', 'firstname')
    if request.method == 'POST':
        conv_id = request.POST['conv_id']
        db_messages = Message.objects.filter(conv_id = conv_id, created_at__date = datetime.now().date())[:]
        return render(request, 'chat/chatroom.html', {'room_name': conv_id, 'db_messages': db_messages, 'conversations': conversations,'user': request.session['user'], 'conversations': conversations,
                                               'avail_users': avail_users,'image_url': os.path.join(str(IMAGE_URL), request.session['user']['profile_pic'])})
    
    return render(request, 'chat/index.html', { 'user': request.session['user'], 'conversations': conversations, 'avail_users': avail_users,
                                               'image_url': os.path.join(str(IMAGE_URL), request.session['user']['profile_pic']), 'chat_img': os.path.join(str(IMAGE_URL), 'chat.jpeg')})   

        

class AddConversationView(generics.GenericAPIView):
    serializer_class = UserIdSerializer
    def post(self, request):
        deserializer = self.serializer_class(data = request.data)
        deserializer.is_valid(raise_exception = True)
        
        seconduser_id = deserializer.validated_data['userId']
        mainuser_id = request.session['user']['id']
        conversation_id = str(mainuser_id) + '-' + str(seconduser_id)
        Conversations.objects.create(mainuser_id = mainuser_id, seconduser_id = seconduser_id, conv_id = conversation_id)
        Conversations.objects.create(mainuser_id = seconduser_id, seconduser_id = mainuser_id, conv_id = conversation_id)
        return Response('Conv Created')
