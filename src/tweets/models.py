from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Q
import os
# Create your models here.

User = get_user_model()


def content_file_name(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class TweetQS(models.query.QuerySet):

    def search(self,query):
        lookup = Q(content__icontains=query) | Q(user__username__icontains=query)
        return self.filter(lookup).distinct()

class TweetModelManager(models.Manager):
    def get_queryset(self):
        return TweetQS(self.model,using=self._db)


    def search(self,query=None):
        return self.get_queryset().search(query)


class Tweet(models.Model):
    user       = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    content    = models.TextField(max_length=140,null=True,blank=True,error_messages={'max_length':'you can write at most 10 characters'})
    image      = models.ImageField(upload_to=content_file_name,null=True,blank=True)
    timestamp  = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True,)

    class Meta:
        verbose_name = 'MyTweet'
        verbose_name_plural = 'tweets'
        ordering=['-timestamp']

    objects = TweetModelManager()
    def get_absolute_url(self):
        # return {'pk'}.format(pk=self.pk)
        return reverse('tweets:detail',kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.id)