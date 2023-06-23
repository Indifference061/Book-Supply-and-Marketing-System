# -*- coding = utf-8 -*-
# @Time : 2023/4/15 17:10
# @Auther : Zoe
# @File : testUrllib .py
# @Software : PyCharm
from django.urls import path, include
from . import views

app_name = 'Userinfo'


urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', views.loginView, name='login'),

    path('logout/', views.logout, name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('userinfo/<int:user_id>/', views.UserInfo.as_view(), name='userinfo'),

]
