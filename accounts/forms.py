from django import forms
from django.contrib.auth.forms import UserCreationForm

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


from accounts.models import User

USER_TYPE = (
    ("Vendor", "Vendor"),
    ("Customer", "Customer"),
)

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control rounded', 'placeholder':'Full Name'}), required=True)
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control rounded', 'placeholder':'Mobile Number'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control rounded' , 'placeholder':'Email Address'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control rounded' , 'placeholder':'Password'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={ 'class': 'form-control rounded' , 'placeholder':'Confirm Password'}), required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    user_type = forms.ChoiceField(choices=USER_TYPE, widget=forms.Select(attrs={"class": "form-select"}))

    class Meta:
        model = User
        fields = ['full_name', 'mobile', 'email', 'password1', 'password2', 'captcha', 'user_type']
       
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control rounded' , 'name': "email", 'placeholder':'Email Address'}), required=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control rounded' , 'name': "password", 'placeholder':'Password'}), required=False)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = User
        fields = ['email', 'password', 'captcha']
