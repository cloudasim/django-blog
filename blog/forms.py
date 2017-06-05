from django import forms
from django.contrib.auth.models import User
from .models import Post


# Form for Blog Posts
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


# Form for Users
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
