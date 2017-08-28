# Inside your app's forms.py file
from django import forms
from datetime import datetime
from django.utils.datastructures import MultiValueDictKeyError
from dateutil.relativedelta import relativedelta
from dateutil import parser
from .models import Users

class RegisterForm(forms.Form):
	name = forms.CharField(max_length=45)
	alias = forms.CharField(max_length=45)
	email = forms.EmailField()
	password = forms.CharField(max_length=100, widget=forms.PasswordInput)
	confirm_password = forms.CharField(max_length=100,widget=forms.PasswordInput)

class LoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(max_length=100, widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
  class Meta:
      model = Users
      fields = ['name', 'alias', 'password']#, except(friends)