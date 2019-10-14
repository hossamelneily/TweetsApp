from django.shortcuts import render
from django.views.generic import View
# Create your views here.
from tweets.models import Tweet


class GetTweets(View):

    def dispatch(self, request, *args, **kwargs):
        # return
        context ={
            'tweets': Tweet.objects.search('#'+kwargs.get('tag_name'))
        }
        return render(request,'tags_home.html',context)