from django.conf.urls import include,url
from .views import Register,ProfileView,ToggleFollow
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy,reverse

app_name = 'accounts'

urlpatterns = [

   # url('login/',Login.as_view(),name='login'),

   url(r'profile/(?P<slug>[\w.@+-]+)/$', ProfileView.as_view(),name='profile'),
   url(r'profile/follow/(?P<slug>[\w.@+-]+)$', ToggleFollow.as_view(), name='Follow'),

   url('register/',Register.as_view(),name='register'),
   url('login/', auth_views.LoginView.as_view(),name='login'),




   url('logout/', auth_views.LogoutView.as_view(), name='logout'),

   url('password_change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('account:password_change_done')), name='password_change'),
   url('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

   url('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
   url('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
   url('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   url('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

