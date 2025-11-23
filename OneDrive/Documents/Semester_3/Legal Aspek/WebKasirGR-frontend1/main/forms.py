from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MerchantRegisterForm(UserCreationForm):
    store_name = forms.CharField(max_length=100, required=True, label="Nama Toko")

    class Meta:
        model = User
        fields = ["username", "store_name", "password1", "password2"]
