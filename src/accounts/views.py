from django.views.generic import CreateView,UpdateView,DetailView,View
from .forms import UserCreationForm,ProfileForm
from django.urls import reverse_lazy,reverse
from django.shortcuts import redirect,render
from django.contrib.auth import  get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from accounts.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
User = get_user_model()

class CustomLoginView(auth_views.LoginView):

    def form_invalid(self, form):
        return render(self.request,'all_tweets.html',{'loginform':form,'registerform':UserCreationForm})

class Register(CreateView):

    form_class = UserCreationForm
    model = User
    template_name = 'registration.html'


    def get_success_url(self):
        return reverse_lazy('accounts:login')

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




class UpdateProfileView(LoginRequiredMixin,UpdateView):

    form_class = ProfileForm
    template_name = 'registration/update_profile.html'


    def get_queryset(self):
        user = User.objects.filter(slug=self.kwargs.get('slug'))
        self.profile_obj = user.first().profile
        return user

    def get_success_url(self):
        return reverse_lazy('tweets:all')

    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial['date_of_birth_year'] = self.profile_obj.date_of_birth.year
    #     print(self.profile_obj.date_of_birth.year)
    #     initial['image'] = self.profile_obj.image
    #     return initial
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['profile_obj'] = self.profile_obj
    #     print(context['form'])
    #     return context

    def form_valid(self, form):
        print(form.cleaned_data)
        user=self.request.user
        try:
            profile_obj = user.profile
        except ObjectDoesNotExist:
            return super().form_invalid(form)
        profile_obj.image=form.cleaned_data.get('image')
        profile_obj.date_of_birth = form.cleaned_data.get('date_of_birth')
        profile_obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_valid(form)




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