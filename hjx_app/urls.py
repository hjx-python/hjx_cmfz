from django.contrib import admin
from django.urls import path
from hjx_app import views

app_name='hjxapp'
urlpatterns=[
    path('index/',views.index,name='show_index'),
    path('login/',views.login,name='show_login'),
    path('loginlogic/',views.login_logic,name='login_logic'),
    path('yzm/',views.code,name='code'),
]