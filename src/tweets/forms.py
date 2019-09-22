from django import forms
from django.contrib.auth import authenticate , login , get_user_model
from .models import Tweet

class TweetForm(forms.ModelForm):


    class Meta:
        model = Tweet
        fields = ['content']
        labels = {
            'content':''
        }

        widgets= {
            'content':forms.Textarea(attrs={'placeholder': 'what\'s in your mind','class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super().__init__(*args, **kwargs)


    def save(self, commit=True):
        instance = super().save(commit=False)
        print(instance)
        if self.request.user:
            instance.user=self.request.user
        instance.save()
        return instance