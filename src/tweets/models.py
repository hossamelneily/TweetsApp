from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Q
from django.db.models.signals import post_save
from Hashtag.models import hashtag

# Create your models here.

User = get_user_model()


def content_file_name(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class TweetQS(models.query.QuerySet):

    def search(self,query):

        # lookup_tweets = Q(content__icontains=query)
        tweets_qs_search = self.filter(content__icontains=query)

        if tweets_qs_search.exists():
            # data['tweets_qs_search']=tweets_qs_search
            return tweets_qs_search
        return Tweet.objects.none()


        # if users_qs_search.exists():
        #     data['users_qs_search'] = users_qs_search
        #
        # if users_qs_search.exists():
        #     data['tags_qs_search'] = tags_qs_search


class TweetModelManager(models.Manager):
    def get_queryset(self):
        return TweetQS(self.model,using=self._db)


    def search(self,query=None):
        return self.get_queryset().search(query)


    def retweet(self,user,parent):
        # if not parent.retweeted:
        return  self.create(
            user=user,
            content=parent.content,
            parent=parent,
            # retweeted = True
        )
        # else:
        #     return None

    def Liked(self,user_obj,tweet_obj):
        print(user_obj.likes.all())
        likes_count = tweet_obj.Liked.count()
        if tweet_obj in user_obj.likes.all():
            if tweet_obj.parent is not None:
                user_obj.likes.remove(tweet_obj)
                user_obj.likes.remove(tweet_obj.parent)
                parent_id = tweet_obj.parent.id
                parent_likes_count = tweet_obj.parent.Liked.count()
            else:
                user_obj.likes.remove(tweet_obj)
                parent_id = 0
                parent_likes_count = 0
            return False , likes_count , parent_id ,parent_likes_count
        else:
            if tweet_obj.parent is not None:
                user_obj.likes.add(tweet_obj)
                user_obj.likes.add(tweet_obj.parent)
                parent_id = tweet_obj.parent.id
                parent_likes_count = tweet_obj.parent.Liked.count()
            else:
                user_obj.likes.add(tweet_obj)
                parent_id = 0
                parent_likes_count = 0
            return True , likes_count , parent_id ,parent_likes_count


class Tweet(models.Model):
    parent     = models.ForeignKey('self',blank=True,null=True,on_delete=models.CASCADE)
    user       = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    content    = models.TextField(max_length=140,null=True,blank=True,error_messages={'max_length':'you can write at most 10 characters'})
    timestamp  = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True,)
    # retweeted  = models.BooleanField(default=False)
    Liked      = models.ManyToManyField(User,blank=True,related_name='likes')
    Reply      = models.BooleanField(default=False,verbose_name='is_a_reply?')

    class Meta:
        verbose_name = 'MyTweet'
        verbose_name_plural = 'tweets'
        ordering=['-timestamp']

    objects = TweetModelManager()
    def get_absolute_url(self):
        # return {'pk'}.format(pk=self.pk)
        return reverse('tweets:detail',kwargs={'pk':self.pk})

    def get_absolute_url_API(self):
        return reverse('api-tweet:detail',kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.id)


# def RetweetPostSaveSignal(sender,instance,created,*args,**kwargs):
#     child = instance
#     if created and child.parent:
#         parent_obj = child.parent
#         parent_obj.retweeted=True
#         parent_obj.save()
#
# post_save.connect(RetweetPostSaveSignal,sender=Tweet)