from .serializers import TweetSerializer, UserSerializer
from rest_framework.generics import ListAPIView,CreateAPIView,ListCreateAPIView,RetrieveAPIView
from rest_framework.views import APIView
from ..models import Tweet
from rest_framework import permissions
from .pagination import LargeResultsSetPagination
from django.contrib.auth import  get_user_model
import re
from Hashtag.models import hashtag
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.exceptions import APIException
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse_lazy,reverse


User = get_user_model()

class TweetSerializerListAPIView(ListAPIView):

    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):  #this get_queryset is called twice
        print("from ajax call")
        if self.kwargs.get('slug') is not None:
            my_tweets = Tweet.objects.filter(user__slug=self.kwargs.get('slug'))
            # user_obj = User.objects.get(slug=self.kwargs.get('slug'))
            # wd=User.objects.all()
            # my_tweets = user_obj.tweet_set.all().order_by('-timestamp') #this will the all() of accounts.profile which is wrong
            return my_tweets

        elif self.kwargs.get('tag_name') is not None:
            tag_name = self.kwargs.get('tag_name')
            hash_tweets = Tweet.objects.search('#'+tag_name)
            return hash_tweets

        elif self.request.GET.get('q') is not None:     # if there is query to be searched for
            # print(self.request.GET.get('q'))
            return Tweet.objects.search(self.request.GET.get('q'))

        else:                                   # if list all the tweets
            qs = Tweet.objects.filter(user__in=self.request.user.profile.get_following())
            my_tweets = self.request.user.tweet_set.all()
            qs =  (qs | my_tweets).distinct().order_by('-timestamp')
            print(qs)
            return qs


class TweetSerializerDetailAPIView(ListAPIView):
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]

    # queryset = Tweet.objects.all()
    def get_queryset(self):

        if self.kwargs.get('pk') is not None:
            tweet_qs = Tweet.objects.filter(pk=self.kwargs.get('pk'))
            tweet_obj = tweet_qs.first()

            if tweet_obj.parent:
                parent_id = tweet_obj.parent.id
                parent_qs = Tweet.objects.filter(id=parent_id)
                children_qs = parent_qs.first().tweet_set.all().order_by('timestamp')
                result_qs = (children_qs | parent_qs).distinct()
            else:
                result_qs = tweet_qs
            # print(tweet_obj)
            # print(children_qs)

            return result_qs

class TweetSerializerCreateAPIView(CreateAPIView):
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        request = self.request
        serializer.save(user=request.user)
        for tag in re.findall('#([\w\d-]+)', request.data.get('content')):
            print(tag)
            obj, created = hashtag.objects.get_or_create(tag='#' + tag)
            obj.count=obj.count+1
            obj.save()

        print("Create API view")
        # print(request.data.get('parent_id'))
        if(request.data.get('isreply')):
            serializer.save(Reply=True)



class LikesTweetsAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        print('like api call ')
        tweet_obj = Tweet.objects.get(id=kwargs.get('id'))
        if tweet_obj is not None:
             print(tweet_obj.id)
             liked,likes_count,parent_object_id,parent_likes_count =Tweet.objects.Liked(request.user,tweet_obj)
             response = Response(
                 {"liked": liked,'likes_count':likes_count,'parent_object_id':parent_object_id,'parent_likes_count':parent_likes_count},
                 content_type="application/json",
             )
             response.accepted_renderer = JSONRenderer()
             response.accepted_media_type = "application/json"
             response.renderer_context = {}
             return response
        raise APIException({'message':"Error in Like API function"})


class RetweetTweetsAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        print('retweet api call ')
        tweet_obj = Tweet.objects.get(id=kwargs.get('pk'))
        if tweet_obj is not None:
             new_tweet =Tweet.objects.retweet(request.user,tweet_obj)
             return HttpResponseRedirect(reverse('tweets:all'))
        raise APIException({'message':"Error in Retweet API function"})


class FollowTweetsAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        user_obj = User.objects.get(slug=kwargs.get('slug'))
        if user_obj is not None:
            if user_obj in request.user.profile.get_following():
                request.user.profile.following.remove(user_obj)
                follow=False
            else:
                request.user.profile.following.add(user_obj)
                follow=True
        print('follow with ajax call')
        following_count = user_obj.profile.get_following().all().count()
        followers_count=  user_obj.followed_by.all().count()
        return JsonResponse({"following_count": following_count, 'followers_count': followers_count,'follow':follow})






