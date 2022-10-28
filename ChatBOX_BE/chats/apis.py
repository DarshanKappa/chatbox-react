from urllib import request
from django.dispatch import receiver
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework import serializers
from .models import UserMessageModel, MessageModel
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class Messageserializer(serializers.ModelSerializer):
    
    class Meta:
        model = MessageModel
        fields = '__all__'

class ChatsSerializer(serializers.ModelSerializer):
        
    message = serializers.SerializerMethodField(read_only=True)
        
    class Meta:
        model = UserMessageModel
        fields = ('id', 'sender', 'receiver', 'message')

    def get_message(self, obj):
        print(Messageserializer(obj.message).data)
        return Messageserializer(obj.message).data

    def to_internal_value(self, data):
        print(data)
        data['sender'] = User.objects.get(pk=data.get('sender'))
        data['receiver'] = User.objects.get(pk=data.get('receiver'))
        message = MessageModel(message=data.get('message'))
        message.save()
        data['message'] = message
        
        return data

class MessageViewset(ListCreateAPIView):
    
    serializer_class = ChatsSerializer
    queryset = UserMessageModel.objects.all()
    
    
class ConversationChatSerializer(serializers.ModelSerializer):
    
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()
    
    class Meta:
        model = UserMessageModel
        fields = ('id', 'sender', 'receiver', 'message')
        
    def get_sender(self, obj):
        se = {'id': obj.sender.id, 'name': obj.sender.first_name}
        return se

    def get_receiver(self, obj):
        re = {'id': obj.receiver.id, 'name': obj.receiver.first_name}
        return re

    def get_message(self, obj):
        msg = {
            'message': obj.message.message,
            'created': {
                'date':obj.message.created.strftime("%d %h,%Y"),
                'time': obj.message.created.strftime("%w:%M %p")
                }
        }
        return msg
    
class ConversationChat(ListAPIView):
    
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    serializer_class = ConversationChatSerializer
    
    def get_queryset(self):
        data = self.request.query_params
        print(data)
        auth_user = self.request.user
        opposite_user = data.get('opposite_user')
        opposite_user = User.objects.get(pk=opposite_user)
        
        queryset = UserMessageModel.objects.filter(Q(Q(sender=auth_user) & Q(receiver=opposite_user))
                                                   | Q(Q(sender=opposite_user) & Q(receiver=auth_user))).order_by('message__created')
        
        return queryset