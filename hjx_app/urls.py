from django.contrib import admin
from django.urls import path
from hjx_app import views

app_name='hjxapp'
urlpatterns=[
    path('index/',views.index,name='show_index'),
    path('login/',views.login,name='show_login'),
    path('loginlogic/',views.login_logic,name='login_logic'),
    path('yzm/',views.code,name='code'),
    path('show_userlist/',views.show_userlist,name="show_userlist"),
    path('update/',views.update,name="update"),
    path('bar_list/',views.bar_list,name="bar_list"),
    path('map_data/',views.map_data,name="map_data"),
]