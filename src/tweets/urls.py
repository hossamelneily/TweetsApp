
from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from django.conf import settings
from django.conf.urls.static import static
from .views import Get_Tweets


app_name="tweets"

urlpatterns = [

    url(r'^',Get_Tweets.as_view(),name='all')
    # url('^cart/', include("cart.urls",namespace="cart")),
]

if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)