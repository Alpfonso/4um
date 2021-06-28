from concurrent.futures import thread
from forum_threads.models import Thread
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.conf.urls import url

from datetime import datetime

import requests
from requests.api import get

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        room_name = self.room_name
        thread_id = room_name[(room_name.rfind('_targ_')):]
        thread_id = thread_id.replace('_targ_', '')

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        #thread_arg_json = json.load(thread_arg)
        thread_arg = ""
        message = text_data_json['user'] + "[" + str(datetime.now().date()) + "|" + str(datetime.now().time().hour)+":"+str(datetime.now().time().minute) + "]:" + text_data_json['message']
        if('thread_arg' in text_data_json):
            thread_arg = text_data_json['thread_arg']
        
            obj_thread = Thread.objects.get(id = int(thread_arg))
            obj_thread.set_lt_content(message)
            obj_thread.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'thread_arg': thread_arg
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        thread_arg = event['thread_arg']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'thread_arg': thread_arg,
        }))