from allauth.account.forms import SignupForm
from django import forms
from diamond.models import UserProfile
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='Firstname')
    last_name = forms.CharField(max_length=30, label='Lastname')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
