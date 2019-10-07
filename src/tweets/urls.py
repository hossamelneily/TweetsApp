
from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static
from .views import GetTweet,DetailTweet,CreateTweet,SearchTweet,DeleteTweet,UpdateTweet


app_name="tweets"

urlpatterns = [

    url(r'^$',GetTweet.as_view(),name='all'),
    url(r'^tweet/(?P<pk>\d+)/$',DetailTweet.as_view(),name='detail'),
    url(r'^tweet/create/$',CreateTweet.as_view(),name='create'),
    url(r'^tweet/delete/(?P<pk>\d+)/$',DeleteTweet.as_view(),name='delete'),
    url(r'^tweet/update/(?P<pk>\d+)/$',UpdateTweet.as_view(),name='update'),
    url(r'^tweet/search/$',SearchTweet.as_view(),name='search'),


]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)