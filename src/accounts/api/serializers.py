from rest_framework import serializers
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django.urls import reverse_lazy,reverse
from ..models import Profile
User=get_user_model()



class FollowedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'following'
        ]
        # model = User
        # fields = [
        #     'username','followed_by'
        # ]
class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
      model = User
      fields =[
          'username'
      ]

class ProfileSerializer(serializers.ModelSerializer):
    following = FollowingSerializer(many=True)
    # followed_by= FollowingSerializer(many=True,read_only=True,source='following')
    date_joined = serializers.SerializerMethodField()
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'image',
            'date_of_birth',
            'date_joined',
            'profile_url',
            'following',
            # 'followed_by',

        ]



    def get_date_joined(self,obj):
        return obj.date_joined.strftime('%b %d  %I:%M %p')


    def get_profile_url(self,obj):
        # return reverse_lazy('api-tweet:profile',kwargs={'slug':obj.user.slug})
        return reverse_lazy('accounts:profile',kwargs={'slug':obj.user.slug})




class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model =  User
        fields = [
            'username',
            'profile'

        ]