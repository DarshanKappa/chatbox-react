from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import User

# Create your models here.



class MessageModel(models.Model):
    
    message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    
class UserMessageModel(models.Model):
    
    sender = models.ForeignKey(User, related_name='sender_message', null=True, on_delete=CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver_message', null=True, on_delete=CASCADE) 
    message = models.ForeignKey(MessageModel, null=True, on_delete=CASCADE)
    
    