from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .validations import user_email_check, username_check
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .models import UserProfile


def email_val(email):
    if user_email_check(email=email):
        raise forms.ValidationError("User already exists")


class UserRegistrationForm(forms.Form):
    firstname = forms.CharField(required=False)
    lastname = forms.CharField(required=False)
    username = forms.CharField(required=True)
    email = forms.EmailField()
    phone = forms.CharField(required=False)
    location = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    is_superuser: bool = False

    def __init__(self, is_superuser: bool = False, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.is_superuser = is_superuser

    def __int__(self, is_superuser: bool = False, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.is_superuser = is_superuser

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        if not self.is_superuser == False:
            raise forms.ValidationError("No superuser")

    def save(self, is_admin: bool = False):
        username = self.cleaned_data['username']
        firstname = self.cleaned_data['firstname']
        lastname = self.cleaned_data['lastname']
        email = self.cleaned_data['email']
        phone = self.cleaned_data['phone']
        location = self.cleaned_data['location']
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        superuser = User.objects.create_superuser if is_admin else User.objects.create_user
        user = superuser(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Eg: Rez'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        if not username_check(cleaned_data['username']):
            self.add_error('username', 'Not Found')
