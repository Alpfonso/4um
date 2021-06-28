from concurrent.futures import thread
from forum_threads.models import Thread
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def room(request):
    room_name = request.GET.get('room_name')
    print(room_name)
    room_name = room_name.replace(" ", "")
    room_name = room_name.replace("@", "")
    context = { # Send context to be used in templates
        'room_name': room_name,
    }
    return render(request, 'room.html', context)