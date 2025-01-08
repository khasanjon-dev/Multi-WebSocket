from django.contrib import admin

from apps.chat.models import Message, Assignment, Mention


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "content", "timestamp", "room_name")
    search_fields = ("sender__username", "content", "room_name")
    list_filter = ("timestamp", "room_name")


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("message", "assigned_to")
    search_fields = ("message__content", "assigned_to__username")
    list_filter = ("assigned_to",)


@admin.register(Mention)
class MentionAdmin(admin.ModelAdmin):
    list_display = ("message", "mentioned_user")
    search_fields = ("message__content", "mentioned_user__username")
    list_filter = ("mentioned_user",)
