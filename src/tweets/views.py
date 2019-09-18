from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from .models import Tweet
from .forms import TweetForm
# Create your views here.




class GetTweet(ListView):

    model = Tweet

    template_name = 'all_tweets.html'



class DetailTweet(DetailView):
    model = Tweet
    template_name = 'detail_tweet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        return context

class CreateTweet(CreateView):
    form_class = TweetForm

    template_name = 'form.html'

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['request'] = self.request
    #     return kwargs


    def form_valid(self, form):
        # form.instance.user = self.request.user
        print(form.instance)
        # self.object = form.save(commit=False)
        # print(dir(form))
        print(form.instance.user)
        # self.object.['user'] = self.request.user
        # self.object.save()
        return super().form_valid(form)







