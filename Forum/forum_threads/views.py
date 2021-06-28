from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Thread, Thread_Comment
from forum_threads.forms import CommentForm

from chat import views
# Create your views here.
import schedule
from forum_threads import keyword_extraction
from pages.models import Profile

def thread_view(request):   # Used to display details about current thread
    obj = Thread.objects.get(id=request.GET.get('id')) # Get object by id
    comment_obj = Thread_Comment(parent_thread = obj)   # Get object by parent id | Thread_Comment model has foreign key from Thread
    queryset = Thread_Comment.objects.filter(parent_thread=comment_obj.parent_thread) # Create queryset for all comments with id
    can_delete = False
    vote_points = Profile.objects.get(username=request.user.username)
    if request.user.username == obj.user.username: # Check if current user is the original Thread poster
        can_delete = True

    no_votes_left = ""
    form = CommentForm(user=request.user, parent=comment_obj.parent_thread)
    if request.method == 'POST':
        if 'comment_form' in request.POST:                                                        # if POST method was received fill in
            form = CommentForm(request.POST, user=request.user, parent=comment_obj.parent_thread)   # form with POST data and also
            if form.is_valid():                                                                     # fill in user and parent data
                form.save() # Save form (if valid) to DB
                form = CommentForm(user=request.user, parent=comment_obj.parent_thread) # Create empty form (except for user and parent)
        if 'vote_form' in request.POST:
            if int(request.POST.get('vote_select')) <= vote_points.vote_amount:
                obj.set_score(int(request.POST.get('vote_select')))
                obj.save()
                vote_points.set_vote_points(int(request.POST.get('vote_select')))
                vote_points.save()
            else:
                no_votes_left = "Not enough votes remaining"

    if obj.live_thread == True:
        room_name = obj.title
        room_name = room_name.replace(" ", "")
        room_name = room_name.replace("@", "")
        room_name = room_name.replace("(", "")
        room_name = room_name.replace(")", "")
        thread_obj = Thread.objects.filter(id = obj.id)
        context = { # Send context to be used in templates
            'room_name': room_name,
            'thread_arg': obj.id,
            'thread_obj': thread_obj,
            'thread': obj,
            'can_delete': can_delete,
            'vote': vote_points,
            'no_votes_left': no_votes_left,
        }
        return render(request, "view_post.html", context)


    
    if request.GET.get('refresh_tags'):
            extracted_tags = keyword_extraction.initialize(obj.description, False)
            thread_sum = keyword_extraction.textrank(obj.description)
            obj.set_thread_summary(thread_sum)
            obj.set_tags(extracted_tags)
            obj.save()


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
        'vote': vote_points,
        'no_votes_left': no_votes_left,
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
