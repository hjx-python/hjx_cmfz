from django.urls import path
from bannerapp import views

app_name='bannerapp'
urlpatterns=[
    # path('index/',views.index,name='show_index'),
    path('banner_list/',views.banner_list,name="banner_list"),
    path('banner_opera/',views.banner_opera,name="banner_opera"),
]