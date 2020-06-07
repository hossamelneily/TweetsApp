from django.conf.urls import url
from .views import GetTweets,GetAllTags


app_name = 'Hashtag'

urlpatterns = [


   url(r'^$', GetAllTags.as_view(),name='all'),

   url(r'(?P<tag_name>([\w\d-]+))/$', GetTweets.as_view(),name='tweets'),



]

