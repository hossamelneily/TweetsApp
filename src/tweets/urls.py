
from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static
from .views import GetTweet,DetailTweet,CreateTweet


app_name="tweets"

urlpatterns = [

    url(r'^$',GetTweet.as_view(),name='all'),
    url(r'^tweet/(?P<pk>\d+)/$',DetailTweet.as_view(),name='detail'),
    url(r'^tweet/create/$',CreateTweet.as_view(),name='create')
]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)