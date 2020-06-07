from django import template
from django.contrib.auth import  get_user_model
from ..models import hashtag
User = get_user_model()
register = template.Library()

@register.inclusion_tag('RecommendedTags.html')
def recommended_tags():
    return {'tags_qs':hashtag.objects.trends()}