from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from nltk.util import pr
from requests.sessions import Request # Import RenderForm from forms.py
from .forms import LoginForm
from forum_threads.forms import ForumForm
from pages.forms import ProfileForm
from forum_threads.models import Thread
from django.core.paginator import Paginator

from .models import Profile
from forum_threads import keyword_extraction

import os, random
from operator import __or__
import django.utils.timezone
# Create your views here.
from django.db.models import Q

def home_view(request, *args, **kwargs):
    if(request.user.username):
        profile = Profile.objects.get(username=request.user.username)

        folder=r"C:\Users\lukas\Desktop\4um\Forum\media"
        img_path=random.choice(os.listdir(folder))
        print(img_path)
        sort_var = "id"
        search_var = ""
        if request.GET.get('sort_type'):
            sort_var = request.GET.get('sort_type')
        if request.GET.get('search_data'):
            search_var = request.GET.get('search_data')
        if request.method == 'POST':
            if 'sort_form' in request.POST:
                sort_var = request.POST.get('sort_select')

        
        if request.GET.get('search_data'):
            queryset = Thread.objects.filter(Q(title__contains=search_var)).order_by(sort_var)
        elif request.GET.get('tag'):
            queryset = Thread.objects.filter(Q(tags__contains=request.GET.get('tag'))) # Check for threads/tags that contain given string
        else:
            queryset = Thread.objects.all().order_by(sort_var)

        paginator = Paginator(queryset, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if str(profile.last_online) != str(django.utils.timezone.datetime.now().date()):
            print(profile.last_online)
            print(str(django.utils.timezone.datetime.now().date()))
            profile.reset_votes()
            profile.set_last_login()
            profile.save()
        context = {
            'page_obj' : page_obj,
            'vote' : profile,
            'sort_var': sort_var,
            'img_path': img_path,
            'search_var': search_var,            
        }
        return render(request, "home.html", context)
    else:
        return redirect("/register")

def profile_view(request, *args, **kwargs):
    user = request.GET.get('user')
    profileQuery = Profile.objects.filter(username=user)
    user_threads = Thread.objects.filter(user = request.user.id)

    paginator = Paginator(user_threads, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    my_context = {
        "profile":profileQuery,
        "user":user,
        "threads": user_threads,
    }
    #userQuerry = Users.objects.filter(username=user)
    if user == request.user.username:
        profile = Profile.objects.get(username = user)
        form = ProfileForm()
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                profile.profile_description = form.cleaned_data.get('profile_description')
                profile.save()
            
        user_tags = profile.get_tags()
        profile_list = []
        if(user_tags):
            try:
                for i in range(5):
                    querry_p = Profile.objects.filter(common_user_tags__contains = user_tags[i])
                    profile_list += [item.username for item in querry_p if item.username not in user]
            except:
                print("No common users found!")
                

        my_context = {
            "profile":profileQuery,
            "user":user,
            "profile_list":list(dict.fromkeys(profile_list)),
            "form":form,
        }
        print(form.fields)

    
    #print(profileQuery)
    
    return render(request, "profile.html", my_context)

def new_post_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = ForumForm(request.POST, user=request.user)
        if form.is_valid():
            extracted_tags = None
            model_instance = form.save()
            obj = Thread.objects.get(id=model_instance.id)
            extracted_tags = keyword_extraction.initialize(model_instance.description, True)
            thread_sum = keyword_extraction.textrank(model_instance.description)
            obj.set_thread_summary(thread_sum)
            obj.set_tags(extracted_tags)
            obj.save()

            profile_obj = Profile.objects.get(username=request.user.username)
            profile_obj.set_tags(extracted_tags)
            profile_obj.save()
            return redirect("/details?id="+str(model_instance.id))
    else:
        form = ForumForm(user=request.user)

    return render(request, "new_post.html", {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            profile = Profile(username = form.cleaned_data.get('username'))
            profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST, data=request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            if(user is not None):
                return redirect('/')
            else:
                print(form.error_messages)
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/register')