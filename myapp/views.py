from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.models import User as UserModel
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import ChatMessage
import json


def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            messages.info(request, f'Account Succesfully created, You can login from here {username}')
            return redirect('chat-login')        
    context = {
        "page":"register",
        'form': form
    }
    return render(request, 'register.html', context)

@login_required
def home(request):
    User = get_user_model()
    users = User.objects.all()
    chats = {}
    chat_id = 0
    if request.method == 'GET' and 'u' in request.GET:
        chats = ChatMessage.objects.filter(Q(user_from=request.user.id, user_to=request.GET['u']) | Q(user_from=request.GET['u'], user_to=request.user.id))
        chats = chats.order_by('date_created')
        chat_id = int(request.GET['u'])
    context = {
        'page':'home',
        'users':users,
        'chats':chats,
        'chat_id' : chat_id
    }
    return render(request, 'home.html', context)

@login_required
def profile(request):
    context = {
        'page':'profile',
        'user':request.user
    }
    return render(request,"profile.html",context)

def get_messages(request):
    chats = ChatMessage.objects.filter(Q(id__gt=request.POST['last_id']),Q(user_from=request.user.id, user_to=request.POST['chat_id']) | Q(user_from=request.POST['chat_id'], user_to=request.user.id))
    new_msgs = []
    for chat in list(chats):
        data = {}
        data['id'] = chat.id
        data['user_from'] = chat.user_from.id
        data['user_to'] = chat.user_to.id
        data['message'] = chat.message
        data['date_created'] = chat.date_created.strftime("%b-%d-%Y %H:%M")
        new_msgs.append(data)
    return HttpResponse(json.dumps(new_msgs), content_type="application/json")

def send_chat(request):
    resp = {}
    User = get_user_model()
    if request.method == 'POST':
        post = request.POST
        u_from = UserModel.objects.get(id=post['user_from'])
        u_to = UserModel.objects.get(id=post['user_to'])
        insert = ChatMessage(user_from=u_from,user_to=u_to,message=post['message'])
        try:
            insert.save()
            resp['status'] = 'success'
        except Exception as ex:
            resp['status'] = 'failed'
            resp['mesg'] = ex
    else:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")