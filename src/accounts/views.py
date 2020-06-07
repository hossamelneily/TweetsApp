from django.views.generic import CreateView,UpdateView,DetailView,View,ListView
from .forms import UserCreationForm,ProfileForm
from django.urls import reverse_lazy,reverse
from django.shortcuts import redirect,render
from django.contrib.auth import  get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from accounts.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from tweets.mixins import NextUrlMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.html import mark_safe
from .models import Profile

User = get_user_model()


class GetAllUsers(ListView):
    model = User
    template_name = 'all_users.html'

    def get_queryset(self):
        return Profile.objects.\
            exclude(user__in=self.request.user.profile.get_following()).\
            exclude(id=self.request.user.id)


class CustomLoginView(NextUrlMixin,auth_views.LoginView):

    # def get_success_url(self):
    #     return redirect((super().get_success_url()))

    # def get_redirect_url(self):
    #     s = super().get_redirect_url()
    #     print(s)

    def form_invalid(self, form):
        return render(self.request,'all_tweets.html',{'loginform':form,'registerform':UserCreationForm})




class Register(SuccessMessageMixin,CreateView):

    form_class = UserCreationForm
    model = User
    template_name = 'registration.html'
    success_message = "%(username)s! your profile was created successfully, please login below to start Tweeting "

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            username=self.object.username.capitalize(),
        )


    def get_success_url(self):
        return reverse_lazy('tweets:all')


    def form_invalid(self, form):
        return render(self.request,'all_tweets.html',{'loginform':AuthenticationForm,'registerform':form})

class ProfileView(LoginRequiredMixin,DetailView):
    model = User
    template_name = 'registration/profile.html'


    # def get_queryset(self):
    #     user = User.objects.filter(slug=self.kwargs.get('slug'))
    #     tweets_qs = user.tweet_set.all()
    #     print(tweets_qs)
    #     return user




class UpdateProfileView(NextUrlMixin,LoginRequiredMixin,UpdateView):

    model = User
    form_class = ProfileForm
    template_name = 'registration/update_profile.html'


    # def get_success_url(self):
    #     if self.get_next_url():
    #         return self.get_next_url()
    #     return redirect(reverse('accounts:profile',kwargs={'slug':self.get_object().slug}))


    def get_initial(self):
        initial = super().get_initial()
        initial['date_of_birth'] = self.get_object().profile.date_of_birth
        initial['image'] = self.get_object().profile.image
        # print(self.get_object().profile.image)
        return initial


    def form_valid(self, form):
        print(form.cleaned_data)

        user=self.request.user
        try:
            profile_obj = user.profile
        except ObjectDoesNotExist:
            return super().form_invalid(form)
        if not form.cleaned_data.get('image'):
            profile_obj.image='mine/empty_pic.jpeg'
        else:
            profile_obj.image=form.cleaned_data.get('image')
        profile_obj.date_of_birth = form.cleaned_data.get('date_of_birth')
        profile_obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)




class ToggleFollow(LoginRequiredMixin,View):


    def dispatch(self, request, *args, **kwargs):
        user_obj = User.objects.get(slug=kwargs.get('slug'))
        if user_obj is not None:
            if user_obj in request.user.profile.get_following():
                request.user.profile.following.remove(user_obj)
            else:
                request.user.profile.following.add(user_obj)
        # return redirect(reverse('accounts:profile',kwargs={'slug':kwargs.get('slug')}))
        # return super().dispatch(request, *args, **kwargs)
        return redirect(request.META['HTTP_REFERER'])