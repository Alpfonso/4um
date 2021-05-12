from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate

from django.contrib.auth.forms import UserCreationForm # Import RenderForm from forms.py
from .forms import LoginForm
from forum_threads.forms import ForumForm
from forum_threads.models import Thread
from django.core.paginator import Paginator

from .models import Profile
from forum_threads import keyword_extraction


# Create your views here.
from django.db.models import Q

def home_view(request, *args, **kwargs):
    vote_points = Profile(username=request.user.username)
    queryset = Thread.objects.all()
    if request.GET.get('tag'):
        queryset = Thread.objects.filter(Q(tags__contains=request.GET.get('tag'))) # Check for threads/tags that contain given string
    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'vote':vote_points
    }
    return render(request, "home.html", context)

def profile_view(request, *args, **kwargs):
    user = request.GET.get('user')
    #userQuerry = Users.objects.filter(username=user)
    if user == request.user.username:
        print("yoyo")
    else:
        print("nono")
    profileQuery = Profile.objects.filter(username=user)
    print(profileQuery)
    my_context = {
        "profile":profileQuery
    }
    return render(request, "profile.html", my_context)

def new_post_view(request, *args, **kwargs):
    form = ForumForm(request.POST, user=request.user)
    extracted_tags = None
    
    confirmation = request.POST.get('radio_tag')
    
    

    if form.is_valid():
        
        model_instance = form.save()
        if confirmation == 'True':
            
            #print("<<--Keyword extraction enabled-->>")
            obj = Thread.objects.get(id=model_instance.id)
            extracted_tags = keyword_extraction.initialize(model_instance.description, True)
            keyword_extraction.textrank(model_instance.description)
            obj.set_tags(extracted_tags)
            obj.save()

            profile_obj = Profile.objects.get(username=request.user.username)
            profile_obj.set_tags(extracted_tags)
            profile_obj.save()
            return redirect("/details?id="+str(model_instance.id))
            #form = ForumForm(request.POST, user=request.user)
        #form = ForumForm(user=request.user)
        return redirect("/")
    return render(request, "new_post.html", {'form': form})

#def register_view(request, *args, **kwargs):
#    return render(request, "register.html", {})

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
            return redirect('/profile')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/profile')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})