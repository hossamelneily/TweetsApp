from rest_framework import serializers
from ..models import hashtag
from django.utils.timesince import timesince


class HashTagSerializer(serializers.ModelSerializer):
    date_display = serializers.SerializerMethodField()
    hashtag_url_API = serializers.SerializerMethodField()
    # last_update = serializers.DateTimeField(source='updated', format='%b %d  %I:%M %p')
    last_update = serializers.SerializerMethodField()

    class Meta:
        model =  hashtag
        fields = [
            'id',
            'tag',
            'count',
            'hashtag_url_API',
            'date_display',
            'last_update',
            'timestamp',
            'updated'

        ]


    def get_date_display(self,obj):
        return obj.timestamp.strftime('%b %d  %I:%M %p')

    def get_last_update(self,obj):
        return timesince(obj.updated).split(',')[0]+' ago'

    def get_hashtag_url_API(self,obj):
        return obj.get_absolute_url_API()

