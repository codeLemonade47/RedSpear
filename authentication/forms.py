from django import forms
from django.forms import ModelForm
from .models import Report
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth.models import User


class IpscanForm(ModelForm):
    class Meta:
        model = Report
        fields = ["ip"]

class CvedesForm(forms.Form):
    cve_id = forms.CharField(max_length=15)


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password")


class SignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['id'] = 'username'
        self.fields['username'].widget.attrs['placeholder'] = 'Enter username'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['id'] = 'password'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter password'