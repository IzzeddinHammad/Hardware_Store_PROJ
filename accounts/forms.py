from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    is_vendor = forms.BooleanField(required=False, label="Sign up as Vendor")

    date_of_birth = forms.DateField(label='Date of Birth' , required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'is_vendor' , 'date_of_birth')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_vendor')