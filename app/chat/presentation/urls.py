from django.urls import path
from chat.presentation.views import (
    ChatRoomView, CoachingChatRoomView, PostSessionFileView)

app_name = 'chat'

urlpatterns = [
    path('room/<int:pk>/', ChatRoomView.as_view(), name='room'),
    path(
        'coach/room/<int:pk>/',
        CoachingChatRoomView.as_view(),
        name='coaching_chat_room'),
    path('session/file/', PostSessionFileView.as_view(), name='session_file'),
]
