from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    # path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('logout/', views.logout_view, name='logout'),
    path('jobs/', views.job_list, name='job-list'),               # GET all jobs
    path('jobs/new/', views.job_create, name='job-create'),       # POST new job
    path('jobs/<int:pk>/edit/', views.job_update, name='job-edit'), # PUT/PATCH update
    path('jobs/<int:pk>/delete/', views.job_delete, name='job-delete'), # DELETE job
    path('chats/', views.chat_page, name='chat_page'),               # shows chat list + default chat
    path('chats/<int:chat_id>/', views.chat_page, name='chat_page'), # select specific chat
    path('chats/start/<int:user_id>/', views.start_chat, name='start_chat'), # start new chat
    path('chats/send/', views.send_message, name='send_message'),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('map/', views.map_view, name='map-view'),
    path('map/add/', views.add_map_item, name='add-map-item'),
    path('map/edit/<int:pk>/', views.edit_map_item, name='edit-map-item'),
    path('map/delete/<int:pk>/', views.delete_map_item, name='delete-map-item'),
    path('profile/', views.profile_view, name='profile'),
    path('chat/', views.chat_view, name='chat'),
    # AJAX endpoints
    path('chats/', views.chat_page, name='chat-list'),  # List users
    path('chat/<str:username>/', views.chat_page, name='chat'),
    path('chats/<str:username>/delete/', views.delete_chat, name='delete_chat'),

]

# urlpatterns = [
#     path('jobs/', views.job_list, name='job-list'),
#     path('jobs/create/', views.job_create_ajax, name='job-create-ajax'),
# ]