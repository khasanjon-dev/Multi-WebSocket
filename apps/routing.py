from django.urls import re_path

from apps.chat import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/all/$", consumers.AllMessagesConsumer.as_asgi()),
    re_path(r"ws/chat/inbox/$", consumers.InboxConsumer.as_asgi()),
    re_path(r"ws/chat/mentions/$", consumers.MentionsConsumer.as_asgi()),
    re_path(r"ws/chat/unassigned/$", consumers.UnassignedConsumer.as_asgi()),
]
