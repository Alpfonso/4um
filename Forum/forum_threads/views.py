from django.shortcuts import render, redirect

from .models import Thread, Thread_Comment
from forum_threads.forms import CommentForm
# Create your views here.

def thread_view(request):   # Used to display details about current thread
    
    id_request = request.GET.get('id')  # Grab parameters from url | templates->home.html ln 9
    #comment_request = request.POST.get()
    obj = Thread.objects.get(id=id_request) # Get object by id
    comment_obj = Thread_Comment(parent_thread = obj)   # Get object by parent id | Thread_Comment model has foreign key from Thread
    queryset = Thread_Comment.objects.filter(parent_thread=comment_obj.parent_thread) # Create queryset for all comments with id
    can_delete = False
    if request.user.username == obj.user: # Check if current user is the original Thread poster
        can_delete = True
    if request.method == 'POST':                                                                # if POST method was received fill in
        form = CommentForm(request.POST, user=request.user, parent=comment_obj.parent_thread)   # form with POST data and also
        if form.is_valid():                                                                     # fill in user and parent data
            form.save() # Save form (if valid) to DB
            form = CommentForm(user=request.user, parent=comment_obj.parent_thread) # Create empty form (except for user and parent)
    else:
        form = CommentForm(user=request.user, parent=comment_obj.parent_thread)
    context = { # Send context to be used in templates
        'thread': obj,
        'form': form,
        "object_list": queryset,
        'can_delete': can_delete
    }
    return render(request, "view_post.html", context)

def thread_delete_view(request):    # Used to delete a thread
    id_request = request.GET.get('id')
    confirmation = request.GET.get('delete')
    if confirmation == "true":
        Thread.objects.filter(id=id_request).delete()
        return redirect('/')
    obj = Thread.objects.get(id=id_request)
    can_delete = False
    if request.user.username == obj.user:
        can_delete = True
    context = {
        'thread': obj,
        'can_delete': can_delete
    }
    return render(request, "view_post.html", context)
