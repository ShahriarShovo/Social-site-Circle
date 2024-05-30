from django.forms import ModelForm
from a_users.models import Profile
from django import forms


class Profileform(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        labels={
            'realname' : 'Name'
        }
        widgets={
            'image':forms.FileInput(),
            'bio':forms.Textarea(attrs={'rows':3})
        }