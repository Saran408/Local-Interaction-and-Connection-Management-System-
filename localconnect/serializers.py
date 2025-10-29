# localconnect/serializers.py
from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    employer_name = serializers.CharField(source='employer.username', read_only=True)
    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'

    def get_timestamp(self, obj):
        return obj.created_at.strftime("%d %b %Y %H:%M")


from .models import ChatRoom, Message

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    time = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'chatroom', 'sender', 'sender_name', 'content', 'time']

    def get_time(self, obj):
        return obj.timestamp.strftime("%d %b %Y, %I:%M %p")

class ChatRoomSerializer(serializers.ModelSerializer):
    user1_name = serializers.CharField(source='user1.username', read_only=True)
    user2_name = serializers.CharField(source='user2.username', read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'user1', 'user1_name', 'user2', 'user2_name', 'created_at', 'last_message']

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        return last_msg.content if last_msg else ""
