from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate

from django.contrib.auth.forms import UserCreationForm # Import RenderForm from forms.py
from .forms import LoginForm
from forum_threads.forms import ForumForm
from forum_threads.models import Thread
from django.core.paginator import Paginator

# Create your views here.

def home_view(request, *args, **kwargs):
    queryset = Thread.objects.all()
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "home.html", {'page_obj': page_obj})

def profile_view(request, *args, **kwargs):
    my_context = {
        "my_text": "This is about me",
        "my_number": 123,
        "list": [1,2,3],
    }
    return render(request, "profile.html", my_context)

def new_post_view(request, *args, **kwargs):
    form = ForumForm(request.POST, user=request.user)
    if form.is_valid():
        form.save()
        form = ForumForm(user=request.user)
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