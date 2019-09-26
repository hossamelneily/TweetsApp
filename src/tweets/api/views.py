from .serializers import TweetSerializer
from rest_framework.generics import ListAPIView,CreateAPIView,ListCreateAPIView
from ..models import Tweet
from rest_framework import permissions
from .pagination import LargeResultsSetPagination
import json
# serializer = SnippetSerializer()



class TweetSerializerListAPIView(ListAPIView):

    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        query = self.request.GET.get('q', '')

        if query is not '':
            qs = Tweet.objects.search(query)
        else:
            qs = Tweet.objects.all()
        print("from ajax call")
        print(qs)
        return qs


class TweetSerializerCreateAPIView(CreateAPIView):
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)







