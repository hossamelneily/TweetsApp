from django.conf.urls import include,url
from .views import Register,ProfileView,ToggleFollow,UpdateProfileView,GetAllUsers
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy,reverse
from .views import CustomLoginView
app_name = 'accounts'

urlpatterns = [


   url(r'related_users/$', GetAllUsers.as_view(),name='all'),
   url(r'profile/(?P<slug>[\w.@+-]+)/$', ProfileView.as_view(),name='profile'),
   url(r'profile/(?P<slug>[\w.@+-]+)/update$', UpdateProfileView.as_view(),name='update_profile'),
   url(r'profile/follow/(?P<slug>[\w.@+-]+)$', ToggleFollow.as_view(), name='Follow'),

   url('register/',Register.as_view(),name='register'),
   url('login/', CustomLoginView.as_view(),name='login'),




   url('logout/', auth_views.LogoutView.as_view(), name='logout'),

   url('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),

   url('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),


]

