from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'main'
# main:login
urlpatterns = [
    path('login/', login_page, name='login'),
    path('signup/', signup, name='signup'),
    path('signhandle/', signhandle, name = 'signhandle'),
    path('loginauth/', loginauth, name = 'loginauth'),
    path('change_password/', change_password, name = 'change_password'),
    path('otp/', otp, name='otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('new_password/', new_password, name='new_password'),
    path('send_friend_request/<int:userID>/', sent_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:requestID>/', accept_friend_request, name='accept_friend_request'),
    path('friend_list/', friend_list, name='friend_list'),
    path('sentrequests/',sentrequests,name='sentrequests'),
    path('recievedrequests/', recievedrequests, name='recievedrequests'),
    
    path('searchhandle/',searchhandle,name='searchhandle'),
    path('search/',autocompletion,name='autocompletion')
]