from django.db import models

# Create your models here.
class hashtagManager(models.Manager):
    def trends(self,limits=7):
        return self.get_queryset().order_by('-count','-updated')[:limits]

class hashtag(models.Model):
    tag = models.CharField(max_length=120)
    count = models.IntegerField(default=0,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tag


    objects=hashtagManager()