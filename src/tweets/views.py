from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,View
from .models import Tweet
from .forms import TweetForm
from django.urls import reverse_lazy,reverse
from django.shortcuts import redirect


class GetTweet(ListView):
    model = Tweet
    template_name = 'all_tweets.html'


    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['create_form'] = TweetForm()
        context['include_url'] = reverse('tweets:create')
        context['btn_title'] = 'Tweet'
        return context






class DetailTweet(DetailView):
    model = Tweet
    template_name = 'detail_tweet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(context)
        return context

class CreateTweet(CreateView):
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




class UpdateTweet(UpdateView):
    form_class = TweetForm
    model = Tweet
    template_name = 'generic_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['btn-value'] = 'Update'
        return context




class DeleteTweet(DeleteView):
    model = Tweet
    success_message = "Deleted Successfully"
    success_url = reverse_lazy('tweets:all')

    template_name = 'form_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['btn-value'] = 'Delete'
        return context




# search form CBV
class SearchTweet(ListView):

    template_name = "all_tweets.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['create_form'] = TweetForm()
        context['include_url'] = reverse('tweets:create')
        context['btn_title'] = 'Tweet'
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            print(query)
            qs = Tweet.objects.search(query)
        else:
            print(query)
            qs = Tweet.objects.all()
        print(qs)
        return qs



class Retweet(View):
    def dispatch(self, request, *args, **kwargs):
        parent_tweet_obj = Tweet.objects.get(pk=kwargs.get('pk'))
        child_tweet_obj = Tweet.objects.retweet(request.user,parent_tweet_obj)
        return redirect(reverse('tweets:all'))

class LikeTweet(View):
    def dispatch(self, request, *args, **kwargs):
        user_obj = Tweet.objects.get(pk=kwargs.get('pk'))
        if user_obj is not None:
            if user_obj in request.user.profile.get_following():
                request.user.profile.following.remove(user_obj)
            else:
                request.user.profile.following.add(user_obj)

        return redirect(reverse('accounts:profile',kwargs={'slug':request.user.slug}))


