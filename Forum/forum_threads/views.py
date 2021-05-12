from django.shortcuts import render, redirect

from .models import Thread, Thread_Comment
from forum_threads.forms import CommentForm

# Create your views here.
import schedule
from forum_threads import keyword_extraction

def thread_view(request):   # Used to display details about current thread
    
    #id_request = request.GET.get('id')  # Grab parameters from url | templates->home.html ln 9
    obj = Thread.objects.get(id=request.GET.get('id')) # Get object by id
    comment_obj = Thread_Comment(parent_thread = obj)   # Get object by parent id | Thread_Comment model has foreign key from Thread
    queryset = Thread_Comment.objects.filter(parent_thread=comment_obj.parent_thread) # Create queryset for all comments with id
    can_delete = False
    if request.user.username == obj.user.username: # Check if current user is the original Thread poster
        can_delete = True
    
    if request.GET.get('refresh_tags'):
            extracted_tags = keyword_extraction.initialize(obj.description, False)
            keyword_extraction.textrank(obj.description)
            obj.set_tags(extracted_tags)


    print(can_delete)

    if request.method == 'POST':                                                                # if POST method was received fill in
        form = CommentForm(request.POST, user=request.user, parent=comment_obj.parent_thread)   # form with POST data and also
        if form.is_valid():                                                                     # fill in user and parent data
            form.save() # Save form (if valid) to DB
            form = CommentForm(user=request.user, parent=comment_obj.parent_thread) # Create empty form (except for user and parent)
    else:
        form = CommentForm(user=request.user, parent=comment_obj.parent_thread)
    if obj.tags != 'False':
        tags = obj.get_tags
    else:
        tags = None
    context = { # Send context to be used in templates
        'thread': obj,
        'form': form,
        "object_list": queryset,
        'can_delete': can_delete,
        'tags':tags,
    }
    return render(request, "view_post.html", context)

def thread_delete_view(request):    # Used to delete a thread
    id_request = request.GET.get('id')
    confirmation = request.GET.get('delete')
    if confirmation == "true":
        Thread.objects.filter(id=id_request).delete()   # On confirmation delete filtered thread
        return redirect('/')                            # and redirect to home
    obj = Thread.objects.get(id=id_request)
    can_delete = False
    if request.user.username == obj.user.username:
        can_delete = True
    context = {
        'thread': obj,
        'can_delete': can_delete
    }
    return render(request, "view_post.html", context)
