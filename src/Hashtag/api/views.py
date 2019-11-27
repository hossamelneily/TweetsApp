from .serializers import HashTagSerializer
from rest_framework.generics import ListAPIView
from rest_framework import permissions
from tweets.api.pagination import LargeResultsSetPagination
from Hashtag.models import hashtag


class HashTagSerializerListAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LargeResultsSetPagination
    serializer_class = HashTagSerializer
    queryset = hashtag.objects.order_by('-count','-updated')