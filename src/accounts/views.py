from django.shortcuts import render
from django.views.generic import CreateView,UpdateView,FormView
from django.contrib.auth.views import LoginView
from .forms import UserCreationForm,ProfileForm
from django.conf import settings
from django.urls import reverse_lazy,reverse
from django.contrib.auth import  get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()


class Register(CreateView):

    form_class = UserCreationForm
    model = User
    template_name = 'registration.html'


    def get_success_url(self):
        return reverse_lazy('accounts:login')



class ProfileView(UpdateView):

    form_class = ProfileForm
    template_name = 'registration/profile.html'


    def get_queryset(self):
        return User.objects.filter(slug=self.kwargs.get('slug'))

    def get_success_url(self):
        return reverse_lazy('accounts:login')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['user'] = self.request.user
    #     print(self.request.user)
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


