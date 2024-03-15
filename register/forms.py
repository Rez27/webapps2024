from django import forms
from .validations import user_email_check, username_check
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


def email_val(email):
    if user_email_check(email=email):
        raise forms.ValidationError("User already exists")


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['password1'].required = True
        self.fields['password2'].required = True

    def save(self, commit=True):
        """
        Saves the user and creates an account for the user

        :param commit:
        :return:
        """
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # if commit:
        #     account = Account(user=user, currency=self.cleaned_data['currency'])
        #     if account.currency != "gbp":
        #         account.balance = convert_currency("GBP", account.currency, 1000)
        user.save()
        # account.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['password'].required = True

