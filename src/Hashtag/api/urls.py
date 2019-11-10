from django.conf.urls import url
from tweets.api.views import TweetSerializerListAPIView
app_name="api"

urlpatterns = [


    ##api serializer
    url(r'(?P<tag_name>([\w\d-]+))/$', TweetSerializerListAPIView.as_view(), name='tags'),

]
