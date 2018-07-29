from django import forms
from .models import Post, UserProfile
from django.contrib.auth import models

class PostModelForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('title', 'content', 'draft', 'image')

class UserProfileModelForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('profile_pic','cover_pic', 'bio', 'website', 'date_of_birth')


class RegisterForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = models.User
		fields = ['username','first_name', 'last_name','email','password']

class LoginForm(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput)