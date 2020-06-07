from rest_framework import serializers,fields
from ..models import Tweet
from accounts.api.serializers import UserSerializer
from django.utils.timesince import timesince

class ParentTweetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    date_display = serializers.DateTimeField(source='timestamp', format='%b %d  %I:%M %p',read_only=True)
    time_since = serializers.SerializerMethodField()
    Tweet_url = serializers.SerializerMethodField()
    Tweet_url_API = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
            'date_display',
            'time_since',
            # 'retweeted',
            'Tweet_url',
            'Tweet_url_API',
            'likes',
            'Reply'


        ]
    # def get_date_display(self,obj):
    #     return obj.timestamp.strftime('%b %d  %I:%M %p')

    def get_time_since(self,obj):
        return timesince(obj.timestamp).split(',')[0]+' ago'

    def get_Tweet_url(self,obj):
        return obj.get_absolute_url()

    def get_Tweet_url_API(self,obj):
        return obj.get_absolute_url_API()

    def get_likes(self,obj):
        # if() + obj.tweet_set.first().Liked.count()
        return obj.Liked.count()



class TweetSerializer(serializers.ModelSerializer):
    parent_id = serializers.CharField(write_only=True, required=False)
    user = UserSerializer(read_only=True)
    parent = ParentTweetSerializer(read_only=True)
    date_display = serializers.DateTimeField(source='timestamp', format='%b %d  %I:%M %p',read_only=True)
    time_since = serializers.SerializerMethodField()
    Tweet_url = serializers.SerializerMethodField()
    Tweet_url_API = serializers.SerializerMethodField()
    likes =  serializers.SerializerMethodField()

    # Reply_to_user_timesince = serializers.CharField(write_only=True,required=False)

    class Meta:
        model =  Tweet
        fields = [
            'parent_id',
            'id',
            'user',
            'content',
            'timestamp',
            'date_display',
            'time_since',
            # 'retweeted',
            'parent',
            'Tweet_url',
            'Tweet_url_API',
            'likes',
            'Reply',

            # 'Reply_to_user_timesince'



        ]
        read_only_fields= ['Reply']

    # def get_date_display(self,obj):
    #     return obj.timestamp.strftime('%b %d  %I:%M %p')

    def get_time_since(self,obj):
        return timesince(obj.timestamp).split(',')[0]+' ago'

    def get_Tweet_url(self,obj):
        return obj.get_absolute_url()

    def get_Tweet_url_API(self,obj):
        return obj.get_absolute_url_API()

    def get_likes(self,obj):
        return obj.Liked.count()