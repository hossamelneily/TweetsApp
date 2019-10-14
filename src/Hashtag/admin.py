from django.contrib import admin

# Register your models here.
from .models import hashtag

class HashAdmin(admin.ModelAdmin):
    readonly_fields = [
        'timestamp'
    ]

admin.site.register(hashtag,HashAdmin)