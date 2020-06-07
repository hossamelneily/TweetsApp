from django.contrib import admin
from .models import Tweet
# Register your models here.

class TweetAdmin(admin.ModelAdmin):

    readonly_fields = ('timestamp','updated')


admin.site.register(Tweet,TweetAdmin)