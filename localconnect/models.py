# localconnect/models.py
from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ]
    CATEGORY_CHOICES = [
        ('sale', 'For Sale'),
        ('exchange', 'Exchange'),
        ('news', 'News'),
        ('meeting', 'Meeting'),
        ('help', 'Help Wanted'),
    ]
    

    
    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    job_type = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    vacancies = models.IntegerField()
    salary = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# class ChatRoom(models.Model):
#     user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user1')
#     user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_user2')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Chat between {self.user1.username} and {self.user2.username}"

# class Message(models.Model):
#     chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.sender.username}: {self.content[:30]}"

# ----------------------------------------------------------------------------------------



# from django.db import models
# from django.contrib.auth.models import User

# class ChatRoom(models.Model):
#     participants = models.ManyToManyField(User, related_name="chatrooms")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"ChatRoom {self.id}"

# class Message(models.Model):
#     room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.sender.username}: {self.content[:20]}"

# ---------------------------------------------------------------------------------------------------






#_________________________________________________________________________________________________
# from django.db import models
# from django.contrib.auth.models import User

# class ChatRoom(models.Model):
#     participants = models.ManyToManyField(User, related_name="chatrooms")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def last_message(self):
#         return self.messages.order_by('-timestamp').first()

#     def __str__(self):
#         return f"ChatRoom {self.id}"


# class Message(models.Model):
#     room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.sender.username}: {self.content[:20]}"
#___________________________________________________________________________________________________________



from django.db import models
from django.contrib.auth.models import User

def upload_to_messages(instance, filename):
    return f"chat_uploads/{instance.sender.username}/{filename}"

class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, related_name='chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        participants_usernames = ', '.join([user.username for user in self.participants.all()])
        return f"Room ({participants_usernames})"


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages_sent', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_to_messages, blank=True, null=True)
    document = models.FileField(upload_to=upload_to_messages, blank=True, null=True)
    video = models.FileField(upload_to=upload_to_messages, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        if self.content:
            return f"{self.sender.username}: {self.content[:20]}"
        elif self.image:
            return f"{self.sender.username} sent an image"
        elif self.document:
            return f"{self.sender.username} sent a document"
        elif self.video:
            return f"{self.sender.username} sent a video"
        return f"{self.sender.username}: Empty message"





















class Post(models.Model):
    CATEGORY_CHOICES = [
        ('sale', 'For Sale'),
        ('exchange', 'Exchange'),
        ('news', 'News'),
        ('meeting', 'Meeting'),
        ('help', 'Help Wanted'),
    ]

    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts_created')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)


    def __str__(self):
        return self.title
    
    
class MapItem(models.Model):
    CATEGORY_CHOICES = [
        ('sale', 'For Sale'),
        ('service', 'Service'),
        ('event', 'Event'),
        ('help', 'Help Wanted'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='map_items/', blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

# models.py
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    # join_date = models.DateField(auto_now_add=True)
    join_date = models.DateField(auto_now_add=True, null=True)


# Signal to create Profile automatically when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
        

