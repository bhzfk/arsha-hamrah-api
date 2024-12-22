from django import forms
from shop_api.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username","first_name","last_name","password"]