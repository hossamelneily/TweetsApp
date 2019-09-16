from django.db import models

# Create your models here.

class Tweet(models.Model):
    text    = models.TextField()



    class Meta:
        verbose_name = 'MyTweet'
        verbose_name_plural = 'tweets'

    def __str__(self):
        return self.text