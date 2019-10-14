from django.conf.urls import include,url
from .views import GetTweets
from django.urls import reverse_lazy,reverse

app_name = 'Hashtag'

urlpatterns = [



   url(r'(?P<tag_name>([\w\d-]+))/$', GetTweets.as_view(),name='tweets'),



]

