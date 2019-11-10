from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,View,TemplateView
from .models import Tweet
from .forms import TweetForm
from django.urls import reverse_lazy,reverse
from django.shortcuts import redirect,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from Hashtag.models import hashtag
from django.shortcuts import render
from django.contrib.auth import  get_user_model


User = get_user_model()
class GetTweet(ListView):     # this is not working as i modified on the all_tweets html
    model = Tweet
    template_name = 'all_tweets.html'


    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['create_form'] = TweetForm()
        context['include_url'] = reverse('tweets:create')
        context['btn_title'] = 'Tweet'
        context['registerform'] = UserCreationForm
        context['loginform'] = AuthenticationForm
        return context






class DetailTweet(LoginRequiredMixin,DetailView):
    model = Tweet
    template_name = 'detail_tweet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        return context

class CreateTweet(LoginRequiredMixin,CreateView):
    form_class = TweetForm
    template_name = 'all_tweets.html'
    success_url = reverse_lazy('tweets:all')

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['create_form'] = TweetForm()
        context['include_url'] = reverse('tweets:create')
        context['btn_title'] = 'Tweet'
        return context

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user

        # if form.instance.content  is not None:
        #     form.instance.content
        return super().form_valid(form)




class UpdateTweet(LoginRequiredMixin,UpdateView):
    form_class = TweetForm
    model = Tweet
    template_name = 'generic_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['btn-value'] = 'Update'
        return context




class DeleteTweet(LoginRequiredMixin,DeleteView):
    model = Tweet
    success_message = "Deleted Successfully"
    success_url = reverse_lazy('tweets:all')

    template_name = 'form_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['btn-value'] = 'Delete'
        return context




# search form CBV
class SearchTweet(LoginRequiredMixin,View):


    def dispatch(self, request, *args, **kwargs):
        query = request.GET.get('q')

        if query and len(query.strip()):
            # print(query)
            query = query.strip()
            lookup_users = Q(username__icontains=query) | Q(email__icontains=query)
            users_qs_search = User.objects.filter(lookup_users).distinct()


            tags_qs_search = hashtag.objects.filter(tag__icontains='#'+query)

            if users_qs_search.exists() or tags_qs_search.exists():
                # print(tags_qs_search)
                return render(request,'search_tweets.html',{'users_qs_search':users_qs_search,'tags_qs_search':tags_qs_search})
            else:
                return render(request,'search_tweets.html',{})

        else:
            return render(request,'search_tweets.html',{})





class Retweet(LoginRequiredMixin,View):
    def dispatch(self, request, *args, **kwargs):
        parent_tweet_obj = Tweet.objects.get(pk=kwargs.get('pk'))
        child_tweet_obj = Tweet.objects.retweet(request.user,parent_tweet_obj)
        return redirect(reverse('tweets:all'))

class LikeTweet(View):
    def dispatch(self, request, *args, **kwargs):
        tweet_obj = Tweet.objects.get(id=kwargs.get('id'))
        if tweet_obj is not None:
            Tweet.objects.Liked(request.user,tweet_obj)
        return redirect(reverse('tweets:all'))

