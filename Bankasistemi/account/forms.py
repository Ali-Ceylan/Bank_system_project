"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Doctor

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('user', 'specialization', 'working_hours')
"""