from django.conf.urls import url
from .views import UsersSerializerListAPIView
from tweets.api.views import TweetSerializerListAPIView
app_name="api"

urlpatterns = [


    ##api serializer
    url(r'^users/$', UsersSerializerListAPIView.as_view(), name='all-users'),
    url(r'profile/(?P<slug>[\w.@+-]+)/$', TweetSerializerListAPIView.as_view(),name='users_tweets'),
]
