from django.conf.urls import url
from tweets.api.views import TweetSerializerListAPIView
from .views import HashTagSerializerListAPIView
app_name="api"

urlpatterns = [


    ##api serializer
    url(r'^$', HashTagSerializerListAPIView.as_view(), name='all'),
    url(r'(?P<tag_name>([\w\d-]+))/$', TweetSerializerListAPIView.as_view(), name='tags'),

]
