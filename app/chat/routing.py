from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/room/(?P<session_id>\d+)/$', consumers.
            ChatConsumer.as_asgi()),
    re_path(r'ws/chat/coach/(?P<coach_id>\d+)/$', consumers.
            CoachChatConsumer.as_asgi()),
]
