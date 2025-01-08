from django.contrib.auth.models import User
from django.db import models


class ChatSession(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.session_id


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=255)  # The room or chat session identifier
    session = models.ForeignKey(
        ChatSession, related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.sender.username} - {self.content[:20]}"


class Assignment(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="assignments"
    )
    assigned_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assignments"
    )

    def __str__(self):
        return f"{self.message.id} assigned to {self.assigned_to.username}"


class Mention(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="mentions"
    )
    mentioned_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mentions"
    )

    def __str__(self):
        return f"{self.message.id} mentioned {self.mentioned_user.username}"
