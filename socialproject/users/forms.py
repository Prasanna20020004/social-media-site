from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginFrom(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, max_length=100)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=100)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def check_passwords(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise forms.ValidationError("Passwords do not match.")
        return self.cleaned_data['confirm_password']
   
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']