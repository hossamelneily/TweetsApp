from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your models here.

User = get_user_model()

class Tweet(models.Model):
    user       = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    content    = models.TextField(max_length=163,null=True,blank=True)
    timestamp  = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True,)

    class Meta:
        verbose_name = 'MyTweet'
        verbose_name_plural = 'tweets'

    def get_absolute_url(self):
        # return {'pk'}.format(pk=self.pk)
        return reverse('tweets:detail',kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.id)