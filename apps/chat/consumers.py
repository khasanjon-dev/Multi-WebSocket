import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from apps.chat.models import Message, Assignment, Mention, ChatSession


class AllMessagesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.room_group_name = f"all_messages_{self.session_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        user = self.scope["user"]

        if data.get("action") == "send_message":
            chat_session = await self.get_or_create_chat_session(self.session_id, user)
            msg = await self.save_message(user, message, chat_session)
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "chat_message", "message": message, "sender": user.username},
            )
        elif data.get("action") == "respond":
            response_message = data["response_message"]
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "response_message",
                    "message": response_message,
                    "sender": user.username,
                },
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"type": "chat_message", **event}))

    async def response_message(self, event):
        await self.send(text_data=json.dumps({"type": "response_message", **event}))

    @sync_to_async
    def save_message(self, user, message, chat_session):
        return Message.objects.create(
            sender=user, content=message, session=chat_session
        )

    @sync_to_async
    def get_or_create_chat_session(self, session_id, user):
        chat_session, created = ChatSession.objects.get_or_create(
            session_id=session_id, defaults={"user": user}
        )
        return chat_session


class InboxConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = f'inbox_{self.scope["user"].username}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_id = data["message_id"]
        user = self.scope["user"]

        await self.assign_message(message_id, user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message_id": message_id,
                "assigned_to": user.username,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def assign_message(self, message_id, user):
        message = Message.objects.get(id=message_id)
        Assignment.objects.create(message=message, assigned_to=user)


class MentionsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = f'mentions_{self.scope["user"].username}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_id = data["message_id"]
        mentioned_username = data["mentioned_username"]
        user = self.scope["user"]

        await self.mention_user(message_id, mentioned_username)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message_id": message_id,
                "mentioned_user": mentioned_username,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def mention_user(self, message_id, mentioned_username):
        message = Message.objects.get(id=message_id)
        mentioned_user = User.objects.get(username=mentioned_username)
        Mention.objects.create(message=message, mentioned_user=mentioned_user)


class UnassignedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "unassigned_messages"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_id = data["message_id"]

        await self.mark_unassigned(message_id)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message_id": message_id,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def mark_unassigned(self, message_id):
        message = Message.objects.get(id=message_id)
        Assignment.objects.filter(message=message).delete()
