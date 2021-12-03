from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages 
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from .forms import *
import json
from django.contrib.auth import get_user_model

User = get_user_model()

from django.conf import settings
from .models import *
from .helpers import *

from django.http import JsonResponse



# Create your views here.
def login_page(request):
    return render(request,'main/login.html')

def loginauth(request):
    if request.method == 'POST':
        e_id = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=e_id, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat_room:home')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('main:login')
    else:
        return redirect('main:login')

def home(request):
    return render(request,'chat_room/home.html')

def autocompletion(request):
    User = get_user_model()
    user = request.GET.get('email')
    emails = []
    # print(user)
    if user:
        user_objs = User.objects.filter(email__contains = user)
        for obj in user_objs:
            emails.append((obj.email))
        # print(emails)
    return JsonResponse({'status':200,'data':emails},safe=False)


def signup(request):
    form = RegisterForm
    para = {
        'form':form
    }
    return render(request, 'main/form.html', context=para)

def signhandle(request):
    if request.method == "POST":
        # Get the post parameters
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['password']
        pass2 = request.POST['password_2']
        dob = request.POST['dob']

        if (pass1!= pass2):
             messages.error(request, " Passwords do not match")
             return redirect('main:signup')
        myuser = User.objects.create_user(email=email, fname=fname, lname=lname, dob=dob, password=pass1)
        myuser.save()
        messages.success(request, " account has been successfully created")
        return redirect('main:login')
    else:
        return redirect('home')

def searchhandle(request):
    if request.method == 'POST':
        email_or_name = request.POST['email']
        user_list = User.objects.filter(email__icontains=email_or_name)
        print(user_list)
        return render(request,'chat_room/results.html', context={'user_list': user_list})
    else:
        return redirect('home')

def change_password(request):
    return render(request, 'main/change_password.html')

def otp(request):
    email = request.POST['email']
    otp = generate_otp()
    try:
        user = User.objects.get(email=email)
    except:
        messages.error(request, "User not found")
    user.otp = otp
    user.save()
    subject, message = generate_otp_mail_fields(otp, user.fname)
    send_mail_helper(subject, message, user.email)
    return render(request, 'main/otp.html', {'email': user.email})

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('my_otp')
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        if str(user.otp) == otp:
            return render(request, 'main/new_password.html', {'email': email})
        else:
            error_message = 'Wrong Otp! Please Try Again.'
            return render(request, 'main/otp.html', {'email': email, 'error': error_message})
    else:
        return redirect('main:login')

def new_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        if password == password_2:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return render(request, 'main/password_changed.html')
        else:
            return render(request, 'main/new_password.html', {'email': email})
    else:
        return redirect('main:login')

def sentrequests(request):
    user = get_user_model()
    all_users = user.objects.all()
    if request.method == 'POST':
        return render(request,'main/add_friends.html', {'allusers': all_users })
    else:
        return redirect('home')


# ----- Creating Views for friend request -------
@login_required
def sent_friend_request(request, userID):
    """Send friend request"""
    from_user = request.user
    to_user = User.objects.get(id=userID)
    friend_request, created = UserRelationShip.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        return render(request, 'main/all_change_redirect.html', {'change': 'Friend request sent'})
    else:
        return render(request, 'main/all_change_redirect.html', {'change': 'Friend request was already sent'})

@login_required
def accept_friend_request(request, requestID):
    """Accept friend request"""
    friend_request = UserRelationShip.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return render(request, 'main/all_change_redirect.html', {'change': 'Friend Request accepted'})
    else:
        return render(request, 'main/all_change_redirect.html', {'change': 'Friend Request not accepted'})

@login_required
def friend_list(request):
    """Returns Friend List page"""
    user_db = User.objects.get(email=request.user)
    all_friends = user_db.friends.all()
    return render(request, 'main/current_friends.html', {
        'all_friends': all_friends
    })

@login_required
def recievedrequests(request):
    user = request.user
    all_friend_requests = UserRelationShip.objects.filter(to_user=user)
    return render(request, 'main/friends_requests.html', {
        'all_friend_requests': all_friend_requests, 
    })