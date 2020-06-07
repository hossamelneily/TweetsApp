from .serializers import  UserSerializer
from rest_framework.generics import ListAPIView
from rest_framework import permissions
from django.contrib.auth import  get_user_model


User = get_user_model()



class UsersSerializerListAPIView(ListAPIView):

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return User.objects.all()



# class WhoToFollowSerializerListAPIView(ListAPIView):
#
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#
#     def get_queryset(self):
#         return User.objects.all()