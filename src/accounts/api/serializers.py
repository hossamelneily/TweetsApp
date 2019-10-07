from rest_framework import serializers
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from ..models import Profile
User=get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ('image', 'date_of_birth')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model =  User
        fields = [
            'username',
            'profile'

        ]