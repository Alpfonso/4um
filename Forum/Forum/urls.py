"""Forum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from Forum.settings import MEDIA_ROOT
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.views.static import serve


from pages.views import home_view, profile_view, register_view, login_view, new_post_view, logout_view
from forum_threads.views import thread_view, thread_delete_view
from chat.views import room

urlpatterns = [
    path('', home_view, name = 'Home'),
    path('profile/', profile_view, name = "Profile"),
    path('register/', register_view, name = "Register"),
    path('login/', login_view, name = "Login"),
    path('logout/', logout_view, name = "Logout"),
    path('post/', new_post_view, name = "New Post"),
    path('details/', thread_view, name = "View Post"),
    path('details/delete_thread', thread_delete_view, name = "Delete Post"),
    path('room/', room, name = "Chat"),
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
