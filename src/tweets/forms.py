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
            'content':forms.Textarea(attrs={'placeholder': 'what\'s in your mind','class':'form-control','id':'TweetTA'}),
        }
        error_messages ={

            'content':{
                'max_length': 'The body of a link post can have at most 10 characters',
            }
        }

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['content'].error_messages = {'max_length': 'Please let us know what to call you!'}



    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     print(instance)
    #     if self.request.user:
    #         instance.user=self.request.user
    #     instance.save()
    #     return instance