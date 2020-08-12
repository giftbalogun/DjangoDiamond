from django import forms
from diamond.models import UserProfile
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from accountprofile.models import Package


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bankname', 'accountname', 'package', 'paid',  'bankacc')


class PackageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('package',)


class PaidForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('paid',)
