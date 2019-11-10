from django.conf.urls import url
from .views import TweetSerializerListAPIView,\
    TweetSerializerCreateAPIView,LikesTweetsAPIView,\
    TweetSerializerDetailAPIView,FollowTweetsAPIView

app_name="api"

urlpatterns = [


    ##api serializer
    url(r'^$', TweetSerializerListAPIView.as_view(), name='all'),
    url(r'^(?P<pk>\d+)/$', TweetSerializerDetailAPIView.as_view(), name='detail'),
    url(r'^search/$', TweetSerializerListAPIView.as_view(), name='search'),
    url(r'^create/$', TweetSerializerCreateAPIView.as_view(), name='create'),
    # url(r'^(?P<slug>[\w.@+-]+)/$', TweetSerializerListAPIView.as_view(), name='profile'),
    # url(r'^users/$', UsersSerializerListAPIView.as_view(), name='all-users'),
    url(r'^(?P<id>\d+)/like$', LikesTweetsAPIView.as_view(), name='tweet-likes'),
    url(r'follow/(?P<slug>[\w.@+-]+)$', FollowTweetsAPIView.as_view(), name='Follow'),
]

