from django.urls import path
from .apis import ConversationChat, MessageViewset


urlpatterns = [
    path('', MessageViewset.as_view(), name='message_view'),
    path('conversation', ConversationChat.as_view(), name='conversation_view'),
    
]