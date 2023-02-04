from django.urls import path
from chat.presentation.views import ChatRoomView

app_name = 'chat'

urlpatterns = [
    path('room/<int:pk>/', ChatRoomView.as_view(), name='room')
]
