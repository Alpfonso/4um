from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    #path('<str:room_name>@<str:thread_arg>/', views.room, name='room'),
]