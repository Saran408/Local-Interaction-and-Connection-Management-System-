# localconnect/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from .forms import JobForm

# # List all jobs
# def job_list(request):
#     jobs = Job.objects.all().order_by('-created_at')
#     return render(request, 'jobs.html', {'jobs': jobs})

# --------------------------------------------------------------------------
#---------------------------------------------------------------------------


#---------------------------------------------------------------------------
#---------------------------------------------------------------------------

# --------------------------------------------------------------------------
from django.shortcuts import render
from .models import Job
from django.db.models import Q


def job_list(request):
    jobs = Job.objects.all()

    # 1. Keyword search
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )

    # 2. Job type filter
    job_type = request.GET.get('job_type')
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    # Send the selected values to template
    context = {
        'jobs': jobs,
        'selected_job_type': job_type or '',
    }
    return render(request, 'jobs.html', context)
# ---------------------------------------------------------------------------

# Post new job
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect('job-list')
    else:
        form = JobForm()
    return render(request, 'job_form.html', {'form': form})

# Edit job
def job_update(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job-list')
    else:
        form = JobForm(instance=job)
    return render(request, 'job_form.html', {'form': form})

# Delete job
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('job-list')
    return render(request, 'job_confirm_delete.html', {'job': job})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatRoom, Message

@login_required
def send_message(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(sender=request.user, text=text)
    return redirect('chat_page')  # Redirect back to the chat page

@login_required
def chat_page(request, chat_id=None):
    user = request.user
    chats = ChatRoom.objects.filter(user1=user) | ChatRoom.objects.filter(user2=user)
    chats = chats.order_by('-created_at')

    if chat_id:
        chatroom = get_object_or_404(ChatRoom, id=chat_id)
        if user not in [chatroom.user1, chatroom.user2]:
            return redirect('chat_page')
    else:
        chatroom = chats.first() if chats.exists() else None

    messages = chatroom.messages.order_by('timestamp') if chatroom else []

    if request.method == 'POST' and chatroom:
        content = request.POST.get('content')
        if content:
            Message.objects.create(chatroom=chatroom, sender=user, content=content)
            return redirect('chat_page', chat_id=chatroom.id)

    return render(request, 'chat/chat_page.html', {
        'chats': chats,
        'chatroom': chatroom,
        'messages': messages,
        'user': user,
    })


@login_required
def start_chat(request, user_id):
    """
    Start a chat with another user.
    Redirect to the existing chatroom if it already exists.
    """
    user2 = get_object_or_404(User, id=user_id)
    user1 = request.user

    if user1 == user2:
        return redirect('chat_page')

    # Check if chatroom already exists
    existing_chat = ChatRoom.objects.filter(user1=user1, user2=user2) | ChatRoom.objects.filter(user1=user2, user2=user1)

    if existing_chat.exists():
        chatroom = existing_chat.first()
    else:
        chatroom = ChatRoom.objects.create(user1=user1, user2=user2)

    return redirect('chat_page', chat_id=chatroom.id)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import PostForm

from django.shortcuts import render
from .models import Post
@login_required
# def home(request):
#     category = request.GET.get('category', '')
#     if category:
#         posts = Post.objects.filter(category=category).order_by('-timestamp')
#     else:
#         posts = Post.objects.all().order_by('-timestamp')
#     return render(request, 'home.html', {'posts': posts, 'selected_category': category})



def home(request):
    posts = Post.objects.all()

    # Search filter
    query = request.GET.get('q')
    if query:
        posts = posts.filter(title__icontains=query)  # or use description__icontains=query

    # Category filter
    selected_category = request.GET.get('category')
    if selected_category:
        posts = posts.filter(category=selected_category)

    context = {
        'posts': posts,
        'selected_category': selected_category,
    }
    return render(request, 'home.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.user:
        post.delete()
    return redirect('home')

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.user:
        return redirect('home')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})


# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from .models import Job
# from .forms import JobForm
# from django.contrib.auth.decorators import login_required
# from django.core import serializers

# @login_required
# def job_list(request):
#     jobs = Job.objects.all().order_by('-created_at')
#     form = JobForm()
#     return render(request, 'jobs.html', {'jobs': jobs, 'form': form})

# @login_required
# def job_create_ajax(request):
#     if request.method == 'POST':
#         form = JobForm(request.POST)
#         if form.is_valid():
#             job = form.save(commit=False)
#             job.employer = request.user
#             job.save()
#             # Return job as JSON
#             data = {
#                 'id': job.id,
#                 'title': job.title,
#                 'type': job.type,
#                 'category': job.category,
#                 'vacancies': job.vacancies,
#                 'salary': job.salary,
#                 'description': job.description,
#                 'location': job.location,
#                 'contact': job.contact,
#                 'employer': job.employer.username,
#                 'timestamp': 'Just now'
#             }
#             return JsonResponse({'status': 'success', 'job': data})
#         else:
#             return JsonResponse({'status': 'error', 'errors': form.errors})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'})





# MAP

from django.shortcuts import render, redirect
from .models import MapItem
from .forms import MapItemForm

def add_map_item(request):
    if request.method == 'POST':
        form = MapItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.posted_by = request.user
            item.save()
            return redirect('map-view')
    else:
        form = MapItemForm()
    return render(request, 'map_item_form.html', {'form': form})

def edit_map_item(request, pk):
    item = MapItem.objects.get(pk=pk)
    if request.method == 'POST':
        form = MapItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('map-view')
    else:
        form = MapItemForm(instance=item)
    return render(request, 'map_item_form.html', {'form': form})

def delete_map_item(request, pk):
    item = MapItem.objects.get(pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('map-view')
    return render(request, 'map_item_confirm_delete.html', {'item': item})

# def map_view(request):
#     items = MapItem.objects.all()
#     return render(request, 'map.html', {'items': items})

from django.shortcuts import render
from .models import Post
from geopy.geocoders import Nominatim

# geolocator = Nominatim(user_agent="localconnect_app")

# def map_view(request):
#     items = Post.objects.all().order_by('-timestamp')  # latest posts first

#     # Prepare items for JS, safely handle missing user
#     items_data = []
#     for post in items:
#         items_data.append({
#             'id': post.id,
#             'title': post.title,
#             'description': post.description,
#             'location': post.location,
#             'category': post.category,
#             'price': post.price,
#             'image': post.image.url if post.image else '',
#             'latitude': post.latitude if hasattr(post, 'latitude') else 20.5937,  # default India center
#             'longitude': post.longitude if hasattr(post, 'longitude') else 78.9629,
#             'user': post.posted_by.username if post.posted_by else "Unknown",
#             'timestamp': post.timestamp,
#         })

#     return render(request, 'map.html', {'items': items_data})










# from django.shortcuts import render
# from .models import Post
# from geopy.geocoders import Nominatim

# def map_view(request):
#     items = Post.objects.all().order_by('-timestamp')  # latest posts first
#     geolocator = Nominatim(user_agent="localconnect")

#     items_data = []
#     for post in items:
#         # Try to get coordinates from location
#         try:
#             location = geolocator.geocode(post.location)
#             if location:
#                 lat = location.latitude
#                 lng = location.longitude
#             else:
#                 # fallback if geocoding fails
#                 lat, lng = 20.5937, 78.9629  # India center
#         except:
#             lat, lng = 20.5937, 78.9629

#         items_data.append({
#             'id': post.id,
#             'title': post.title,
#             'description': post.description,
#             'location': post.location,
#             'category': post.category,
#             'price': post.price,
#             'image': post.image.url if post.image else '',
#             'latitude': lat,
#             'longitude': lng,
#             'user': post.posted_by.username if post.posted_by else "Unknown",
#             'timestamp': post.timestamp,
#         })

#     return render(request, 'map.html', {'items': items_data})





from django.shortcuts import render
from .models import Post
from geopy.geocoders import Nominatim

def map_view(request):
    items = Post.objects.all().order_by('-timestamp')  # latest posts first
    geolocator = Nominatim(user_agent="localconnect")

    items_data = []
    for post in items:
        try:
            location = geolocator.geocode(post.location)
            if location:
                lat = location.latitude
                lng = location.longitude
            else:
                lat, lng = 20.5937, 78.9629  # India center fallback
        except:
            lat, lng = 20.5937, 78.9629

        items_data.append({
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'location': post.location,
            'category': post.category,
            'price': post.price,
            'image': post.image.url if post.image else '',
            'latitude': lat,
            'longitude': lng,
            'user': post.user.username if post.user else "Unknown",  # ✅ FIXED
            'timestamp': post.timestamp,
        })

    return render(request, 'map.html', {'items': items_data})

















# from django.shortcuts import render
# from django.urls import reverse
# from .models import Post
# from geopy.geocoders import Nominatim

# def map_view(request):
#     items = Post.objects.all().order_by('-timestamp')  # latest posts first
#     geolocator = Nominatim(user_agent="localconnect")

#     items_data = []
#     for post in items:
#         # Get coordinates from location
#         try:
#             location = geolocator.geocode(post.location)
#             if location:
#                 lat = location.latitude
#                 lng = location.longitude
#             else:
#                 lat, lng = 20.5937, 78.9629  # India center fallback
#         except:
#             lat, lng = 20.5937, 78.9629

#         # Get username safely
#         username = getattr(post.posted_by, 'username', None)
        
#         # Build chat URL if username exists
#         if username:
#             try:
#                 chat_url = reverse('chat', kwargs={'username': username})
#             except:
#                 chat_url = None
#         else:
#             chat_url = None

#         items_data.append({
#             'id': post.id,
#             'title': getattr(post, 'title', ''),
#             'description': getattr(post, 'description', ''),
#             'location': getattr(post, 'location', ''),
#             'category': getattr(post, 'category', ''),
#             'price': getattr(post, 'price', ''),
#             'image': post.image.url if getattr(post, 'image', None) else '',
#             'latitude': lat,
#             'longitude': lng,
#             'user': username or "Unknown",
#             'chat_url': chat_url,
#             'timestamp': getattr(post, 'timestamp', None),
#         })

#     return render(request, 'map.html', {'items': items_data})

















# def index(request):
#     return render(request, 'index.html')

from django.shortcuts import render, redirect

def index(request):
    # If user is logged in, redirect to the main home/dashboard page
    if request.user.is_authenticated:
        return redirect('home')  # your main home page URL name
    return render(request, 'index.html')


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth.models import User

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']

            # Allow login via username or email
            try:
                user_obj = User.objects.get(email=username_or_email)
                username = user_obj.username
            except User.DoesNotExist:
                username = username_or_email

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to your home page
            else:
                form.add_error(None, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm
from .models import Profile 

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # # Create Profile with extra fields
            # Profile.objects.create(user=user, location=form.cleaned_data['location'])
            
            # You can save location in Profile if using extended user
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm




from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to landing page after logout



# # views.py
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Profile, Job
# from .forms import ProfileForm  # We'll create this form

# @login_required
# def profile_page(request):
#     profile, created = Profile.objects.get_or_create(user=request.user)
#     user_jobs = Job.objects.filter(employer=request.user).order_by('-created_at')
    
#     if request.method == "POST":
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')  # reload page after save
#     else:
#         form = ProfileForm(instance=profile)

#     context = {
#         'profile': profile,
#         'user_jobs': user_jobs,
#         'form': form,
#     }
#     return render(request, 'profile.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Job
from .forms import ProfileForm

@login_required
def profile_view(request):
    profile = request.user.profile

    # Fix: filter jobs by 'employer' instead of 'user'
    user_jobs = Job.objects.filter(employer=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            # Update User model fields
            request.user.username = form.cleaned_data['username']
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()

            return redirect('profile')
    else:
        # Pre-fill form fields from User and Profile
        form = ProfileForm(instance=profile, initial={
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })

    context = {
        'profile': profile,
        'user_jobs': user_jobs,
        'form': form,
    }
    return render(request, 'profile.html', context)


@login_required
def chat_view(request):
    """Renders the chat page only for logged-in users."""
    return render(request, 'chat\chat_page.html')


# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404

# @login_required
# def send_message(request):
#     """
#     Accepts POST with 'chat_id' and 'content'.
#     Works for regular POST (form) and also returns JSON if requested via fetch.
#     """
#     if request.method == 'POST':
#         chat_id = request.POST.get('chat_id') or request.GET.get('chat_id')
#         content = request.POST.get('content') or request.POST.get('text') or request.GET.get('content')
#         if chat_id and content:
#             chatroom = get_object_or_404(ChatRoom, id=chat_id)
#             msg = Message.objects.create(chatroom=chatroom, sender=request.user, content=content)
#             # If AJAX request - return the created message as JSON
#             if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
#                 return JsonResponse({
#                     'id': msg.id,
#                     'sender': msg.sender.username,
#                     'content': msg.content,
#                     'timestamp': msg.timestamp.isoformat()
#                 })
#     # fallback redirect for non-AJAX form post
#     return redirect('chat_page')


# from django.http import JsonResponse

# @login_required
# def chat_messages_json(request, chat_id):
#     chatroom = get_object_or_404(ChatRoom, id=chat_id)
#     qs = chatroom.messages.order_by('timestamp').select_related('sender')
#     data = []
#     for m in qs:
#         data.append({
#             'id': m.id,
#             'sender': m.sender.username,
#             'content': m.content,
#             'timestamp': m.timestamp.isoformat(),
#             'mine': m.sender == request.user
#         })
#     return JsonResponse({'messages': data})


# ------------------------------------------------------------------------------------------------------------
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.models import User
# from .models import ChatRoom, Message

# def chat_page(request, username=None):
#     current_user = request.user

#     # ✅ Handle new message POST
#     if request.method == "POST" and username:
#         other_user = get_object_or_404(User, username=username)
#         room = ChatRoom.objects.filter(participants=current_user).filter(participants=other_user).first()
#         if not room:
#             room = ChatRoom.objects.create()
#             room.participants.add(current_user, other_user)

#         content = request.POST.get("content")
#         if content:
#             Message.objects.create(room=room, sender=current_user, content=content)
#         return redirect("chat", username=username)

#     # ✅ Fetch or create room for GET
#     room = None
#     if username:
#         other_user = get_object_or_404(User, username=username)
#         room = ChatRoom.objects.filter(participants=current_user).filter(participants=other_user).first()
#         if not room:
#             room = ChatRoom.objects.create()
#             room.participants.add(current_user, other_user)

#     messages = room.messages.all() if room else []
#     users = User.objects.exclude(id=current_user.id)  # List of other users

#     context = {
#         "room": room,
#         "messages": messages,
#         "users": users,
#         "other_user": username,
#     }
#     return render(request, "chat/chat_page.html", context)

# -------------------------------------------------------------------------------------------------






# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.db.models import Max
# from .models import ChatRoom, Message

# @login_required
# def chat_page(request, username=None):
#     current_user = request.user

#     # Handle POST: sending a message
#     if request.method == "POST" and username:
#         other_user = get_object_or_404(User, username=username)
#         room = ChatRoom.objects.filter(participants=current_user).filter(participants=other_user).first()
#         if not room:
#             room = ChatRoom.objects.create()
#             room.participants.add(current_user, other_user)

#         content = request.POST.get("content")
#         if content:
#             Message.objects.create(room=room, sender=current_user, content=content)
#         return redirect("chat", username=username)

#     # Get or create room for GET
#     room = None
#     if username:
#         other_user = get_object_or_404(User, username=username)
#         room = ChatRoom.objects.filter(participants=current_user).filter(participants=other_user).first()
#         if not room:
#             room = ChatRoom.objects.create()
#             room.participants.add(current_user, other_user)

#         # Mark unread messages as read
#         room.messages.filter(is_read=False).exclude(sender=current_user).update(is_read=True)

#     messages = room.messages.order_by('timestamp') if room else []

#     # List all chat rooms of current user, ordered by last message
#     chat_rooms = current_user.chatrooms.annotate(last_msg_time=Max('messages__timestamp')).order_by('-last_msg_time')

#     # Prepare tuples (room, other_user, unread_count)
#     chat_rooms_with_users = []
#     for r in chat_rooms:
#         other = r.participants.exclude(id=current_user.id).first()
#         unread_count = r.messages.filter(is_read=False).exclude(sender=current_user).count()
#         chat_rooms_with_users.append((r, other, unread_count))

#     # List of other users to start new chat
#     users = User.objects.exclude(id=current_user.id)

#     context = {
#         "room": room,
#         "messages": messages,
#         "chat_rooms": chat_rooms_with_users,
#         "users": users,
#         "other_user": username,
#     }
#     return render(request, "chat/chat_page.html", context)














# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.db.models import Max
# from .models import ChatRoom, Message

# @login_required
# def chat_page(request, username=None):
#     current_user = request.user

#     # Handle POST: sending a message
#     if request.method == "POST" and username:
#         other_user = get_object_or_404(User, username=username)
#         room = ChatRoom.objects.filter(participants=current_user).filter(participants=other_user).first()
#         if not room:
#             room = ChatRoom.objects.create()
#             room.participants.add(current_user, other_user)

#         content = request.POST.get("content")
#         if content:
#             Message.objects.create(room=room, sender=current_user, content=content)
#         return redirect("chat", username=username)

#     # GET request
#     room = None
#     other_user_obj = None
#     if username:
#         other_user_obj = get_object_or_404(User, username=username)
#         room = ChatRoom.objects.filter(participants=current_user).filter(participants=other_user_obj).first()
#         if not room:
#             room = ChatRoom.objects.create()
#             room.participants.add(current_user, other_user_obj)

#         # Mark unread messages as read
#         room.messages.filter(is_read=False).exclude(sender=current_user).update(is_read=True)

#     messages = room.messages.order_by('timestamp') if room else []

#     # List all chat rooms of current user, ordered by last message
#     chat_rooms = current_user.chatrooms.annotate(last_msg_time=Max('messages__timestamp')).order_by('-last_msg_time')

#     # Prepare tuples (room, other_user, unread_count)
#     chat_rooms_with_users = []
#     for r in chat_rooms:
#         other = r.participants.exclude(id=current_user.id).first()
#         unread_count = r.messages.filter(is_read=False).exclude(sender=current_user).count()
#         chat_rooms_with_users.append((r, other, unread_count))

#     # List of other users to start new chat
#     users = User.objects.exclude(id=current_user.id)

#     context = {
#         "room": room,
#         "messages": messages,
#         "chat_rooms": chat_rooms_with_users,
#         "users": users,
#         "other_user_obj": other_user_obj,  # Pass the user object for header
#     }
#     return render(request, "chat/chat_page.html", context)







# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.db.models import Max, Q
# from .models import ChatRoom, Message
# from .forms import MessageForm

# @login_required
# def chat_page(request, username=None):
#     current_user = request.user

#     # Search functionality
#     search_query = request.GET.get('search', '')
#     users = User.objects.exclude(id=current_user.id)
#     if search_query:
#         users = users.filter(username__icontains=search_query)

#     # Handle POST: sending message
#     if request.method == "POST" and username:
#         other_user = get_object_or_404(User, username=username)
#         room = ChatRoom.objects.filter(participants=current_user).filter(participants=other_user).first()
#         if not room:
#             room = ChatRoom.objects.create()
#             room.participants.add(current_user, other_user)

#         form = MessageForm(request.POST, request.FILES)
#         if form.is_valid():
#             msg = form.save(commit=False)
#             msg.sender = current_user
#             msg.room = room
#             msg.save()
#         return redirect("chat", username=username)

#     # GET request
#     room = None
#     other_user_obj = None
#     if username:
#         other_user_obj = get_object_or_404(User, username=username)
#         room = ChatRoom.objects.filter(participants=current_user).filter(participants=other_user_obj).first()
#         if not room:
#             room = ChatRoom.objects.create()
#             room.participants.add(current_user, other_user_obj)

#         # Mark unread messages as read
#         room.messages.filter(is_read=False).exclude(sender=current_user).update(is_read=True)

#     messages = room.messages.order_by('timestamp') if room else []

#     # List all chat rooms of current user, ordered by last message
#     chat_rooms = current_user.chatrooms.annotate(last_msg_time=Max('messages__timestamp')).order_by('-last_msg_time')

#     # Prepare tuples (room, other_user, unread_count)
#     chat_rooms_with_users = []
#     for r in chat_rooms:
#         other = r.participants.exclude(id=current_user.id).first()
#         unread_count = r.messages.filter(is_read=False).exclude(sender=current_user).count()
#         chat_rooms_with_users.append((r, other, unread_count))

#     context = {
#         "room": room,
#         "messages": messages,
#         "chat_rooms": chat_rooms_with_users,
#         "users": users,
#         "other_user_obj": other_user_obj,
#         "search_query": search_query,
#         "form": MessageForm(),
#     }
#     return render(request, "chat/chat_page.html", context)

# @login_required
# def delete_chat(request, username):
#     other_user = get_object_or_404(User, username=username)
#     room = ChatRoom.objects.filter(participants=request.user).filter(participants=other_user).first()
#     if room:
#         room.delete()
#     return redirect("chat-list")









# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.db.models import Max, Q
# from .models import ChatRoom, Message
# from .forms import MessageForm

# @login_required
# def chat_page(request, username=None):
#     current_user = request.user

#     # Handle POST: sending a message with files
#     if request.method == "POST" and username:
#         other_user = get_object_or_404(User, username=username)
#         room = ChatRoom.objects.filter(participants=current_user).filter(participants=other_user).first()
#         if not room:
#             room = ChatRoom.objects.create()
#             room.participants.add(current_user, other_user)

#         form = MessageForm(request.POST, request.FILES)
#         if form.is_valid():
#             msg = form.save(commit=False)
#             msg.sender = current_user
#             msg.room = room
#             msg.save()
#         return redirect("chat", username=username)

#     # GET request
#     room = None
#     other_user_obj = None
#     if username:
#         other_user_obj = get_object_or_404(User, username=username)
#         room = ChatRoom.objects.filter(participants=current_user).filter(participants=other_user_obj).first()
#         if not room:
#             room = ChatRoom.objects.create()
#             room.participants.add(current_user, other_user_obj)

#         # Mark unread messages as read
#         room.messages.filter(is_read=False).exclude(sender=current_user).update(is_read=True)

#     messages = room.messages.order_by('timestamp') if room else []

#     # List all chat rooms of current user, ordered by last message
#     chat_rooms = current_user.chatrooms.annotate(last_msg_time=Max('messages__timestamp')).order_by('-last_msg_time')

#     chat_rooms_with_users = []
#     for r in chat_rooms:
#         other = r.participants.exclude(id=current_user.id).first()
#         unread_count = r.messages.filter(is_read=False).exclude(sender=current_user).count()
#         chat_rooms_with_users.append((r, other, unread_count))

#     # **List all users except current user (for search)**
#     users = User.objects.exclude(id=current_user.id)

#     context = {
#         "room": room,
#         "messages": messages,
#         "chat_rooms": chat_rooms_with_users,
#         "users": users,
#         "other_user_obj": other_user_obj,
#         "message_form": MessageForm(),
#     }
#     return render(request, "chat/chat_page.html", context)

# from django.contrib import messages
# @login_required
# def delete_chat(request, username):
#     current_user = request.user
#     other_user = get_object_or_404(User, username=username)
#     room = ChatRoom.objects.filter(participants=current_user).filter(participants=other_user).first()
    
#     if room:
#         room.delete()
#         messages.success(request, f"Chat with {other_user.username} has been deleted.")
#     else:
#         messages.warning(request, "No chat found to delete.")

#     return redirect('chat-list')















from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max, Q
from .models import ChatRoom, Message

@login_required
def chat_page(request, username=None):
    current_user = request.user
    search_query = request.GET.get('search', '').strip()

    # Handle POST: sending messages
    if request.method == "POST" and username:
        other_user = get_object_or_404(User, username=username)
        room = ChatRoom.objects.filter(participants=current_user).filter(participants=other_user).first()
        if not room:
            room = ChatRoom.objects.create()
            room.participants.add(current_user, other_user)

        content = request.POST.get("content")
        image = request.FILES.get("image")
        document = request.FILES.get("document")
        video = request.FILES.get("video")

        if content or image or document or video:
            Message.objects.create(
                room=room,
                sender=current_user,
                content=content,
                image=image,
                document=document,
                video=video
            )
        return redirect("chat", username=username)

    # GET request: current room
    room = None
    other_user_obj = None
    if username:
        other_user_obj = get_object_or_404(User, username=username)
        room = ChatRoom.objects.filter(participants=current_user).filter(participants=other_user_obj).first()
        if not room:
            room = ChatRoom.objects.create()
            room.participants.add(current_user, other_user_obj)
        # Mark messages as read
        room.messages.filter(is_read=False).exclude(sender=current_user).update(is_read=True)

    messages = room.messages.order_by('timestamp') if room else []

    # All users except current
    all_users = User.objects.exclude(id=current_user.id)

    # Existing chat rooms with last message
    chat_rooms_qs = current_user.chatrooms.annotate(last_msg_time=Max('messages__timestamp')).order_by('-last_msg_time')
    chat_rooms_list = []
    chatted_usernames = []

    for r in chat_rooms_qs:
        other = r.participants.exclude(id=current_user.id).first()
        last_msg = r.messages.last()
        unread_count = r.messages.filter(is_read=False).exclude(sender=current_user).count()
        chat_rooms_list.append((r, other, last_msg, unread_count))
        chatted_usernames.append(other.username)

    # Users not yet chatted
    unchatted_users = all_users.exclude(username__in=chatted_usernames)

    # Filter based on search query
    if search_query:
        chat_rooms_list = [
            (r, other, last_msg, unread_count)
            for r, other, last_msg, unread_count in chat_rooms_list
            if search_query.lower() in other.username.lower()
        ]
        unchatted_users = unchatted_users.filter(username__icontains=search_query)

    # Add unchatted users at the end with room=None
    for u in unchatted_users:
        chat_rooms_list.append((None, u, None, 0))

    context = {
        "room": room,
        "messages": messages,
        "chat_rooms": chat_rooms_list,
        "other_user_obj": other_user_obj,
    }
    return render(request, "chat/chat_page.html", context)


@login_required
def delete_chat(request, username):
    current_user = request.user
    other_user = get_object_or_404(User, username=username)
    room = ChatRoom.objects.filter(participants=current_user).filter(participants=other_user).first()
    if room:
        room.delete()
    return redirect("chat-list")
