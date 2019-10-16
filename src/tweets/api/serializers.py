from rest_framework import serializers,fields
from ..models import Tweet
from accounts.api.serializers import UserSerializer
from django.utils.timesince import timesince

class ParentTweetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    date_display = serializers.SerializerMethodField()
    time_since = serializers.SerializerMethodField()
    Tweet_url = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [

            'user',
            'content',
            'date_display',
            'time_since',
            'retweeted',
            'Tweet_url'


        ]
    def get_date_display(self,obj):
        return obj.timestamp.strftime('%b %d  %I:%M %p')

    def get_time_since(self,obj):
        return timesince(obj.timestamp).split(',')[0]+' ago'

    def get_Tweet_url(self,obj):
        return obj.get_absolute_url()

class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    parent = ParentTweetSerializer(read_only=True)
    date_display = serializers.SerializerMethodField()
    time_since = serializers.SerializerMethodField()
    Tweet_url = serializers.SerializerMethodField()
    class Meta:
        model =  Tweet
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
            'date_display',
            'time_since',
            'retweeted',
            'parent',
            'Tweet_url'

        ]

    def get_date_display(self,obj):
        return obj.timestamp.strftime('%b %d  %I:%M %p')

    def get_time_since(self,obj):
        return timesince(obj.timestamp).split(',')[0]+' ago'

    def get_Tweet_url(self,obj):
        return obj.get_absolute_url()