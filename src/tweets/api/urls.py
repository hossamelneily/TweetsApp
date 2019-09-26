
from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static
from .views import TweetSerializerListAPIView,TweetSerializerCreateAPIView

app_name="api"

urlpatterns = [


    ##api serializer
    url(r'^$', TweetSerializerListAPIView.as_view(), name='all'),
    url(r'^create/$', TweetSerializerCreateAPIView.as_view(), name='create'),

]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)