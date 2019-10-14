from .serializers import TweetSerializer,UserSerializer
from rest_framework.generics import ListAPIView,CreateAPIView,ListCreateAPIView,RetrieveAPIView
from ..models import Tweet
from rest_framework import permissions
from .pagination import LargeResultsSetPagination
from django.contrib.auth import  get_user_model
import json
import re
from Hashtag.models import hashtag
# serializer = SnippetSerializer()

User = get_user_model()

class TweetSerializerListAPIView(ListAPIView):

    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        if self.kwargs.get('slug') is not None:
            my_tweets = self.request.user.tweet_set.all()
            return my_tweets
        else:
            query = self.request.GET.get('q')
            print(query)
            if query is not None:                   # if there is query to be searched for
                qs = Tweet.objects.search(query)
            else:                                   # if list all the tweets
                qs = Tweet.objects.filter(user__in=self.request.user.profile.get_following())
                my_tweets = self.request.user.tweet_set.all()
                qs =  (qs | my_tweets).distinct().order_by('-timestamp')
            print("from ajax call")
            print(qs)
            return qs


class TweetSerializerCreateAPIView(CreateAPIView):
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # print(self.request.data)
        for tag in re.findall('#([\w\d-]+)', self.request.data.get('content')):
            print(tag)
            obj, created = hashtag.objects.get_or_create(tag='#' + tag)


# class ProfileTweetSerializerRetrieveAPIView(RetrieveAPIView):
#
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#
#     def get_object(self):
#         return User.objects.get(slug=self.kwargs.get('slug'))





