# # localconnect/admin.py
# from django.contrib import admin
# from .models import Job

# @admin.register(Job)
# class JobAdmin(admin.ModelAdmin):
#     list_display = ('title', 'employer', 'job_type', 'category', 'vacancies', 'salary', 'created_at')
#     list_filter = ('job_type', 'category', 'employer')
#     search_fields = ('title', 'description', 'location', 'employer__username')


# admin.site.register(Job)
# admin.site.register(ChatRoom)
# admin.site.register(Message)
# admin.site.register(Post)

from django.contrib import admin
from .models import Job, ChatRoom, Message, Post,MapItem  # ✅ Import all models


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'job_type', 'category', 'vacancies', 'salary', 'created_at')
    list_filter = ('job_type', 'category', 'employer')
    search_fields = ('title', 'description', 'location', 'employer__username')


# ✅ Register other models
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(Post)
admin.site.register(MapItem)