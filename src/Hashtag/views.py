from django.shortcuts import render
from django.views.generic import View,ListView
# Create your views here.
from tweets.models import Tweet
from .models import hashtag

class GetAllTags(ListView):
    model = hashtag
    template_name = 'all_tags.html'


class GetTweets(View):

    def dispatch(self, request, *args, **kwargs):
        # return
        context ={
            'tweets': Tweet.objects.search('#'+kwargs.get('tag_name'))
        }
        return render(request,'tags_home.html',context)