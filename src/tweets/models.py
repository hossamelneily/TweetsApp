from django.db import models
from django.utils import timezone
from django.conf import settings
# Create your models here.


class Tweet(models.Model):

    content    = models.TextField(max_length=163,null=True,blank=True)
    timestamp  = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True,)

    class Meta:
        verbose_name = 'MyTweet'
        verbose_name_plural = 'tweets'

    def __str__(self):
        return str(self.id)