from django import template
from django.contrib.auth import  get_user_model
from accounts.models import Profile
User = get_user_model()
register = template.Library()

@register.inclusion_tag('RecommendedUsers.html')
def recommended_users(user):
    if isinstance(user,User):
        return {'profile_qs':Profile.objects.recommended(user)}