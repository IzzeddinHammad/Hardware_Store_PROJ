from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser



class CustomUserCreationForm(UserCreationForm):
    is_vendor = forms.BooleanField(required=True, label="Sign up as Vendor")

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email','is_vendor')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = fields = ('username', 'email',)


