from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Tweet
# Create your views here.




class Get_Tweets(ListView):

    model = Tweet

    template_name = 'all_tweets.html'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(Get_Tweets, self).get_context_data()
    #     return context
